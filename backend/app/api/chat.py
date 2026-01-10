from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload
from typing import Optional
import uuid

from ..database import get_db
from ..models.chat_message import ChatMessage
from ..models.chronicle import Chronicle, ChronicleMember
from ..models.character import Character
from ..models.game_session import GameSession
from ..models.user import User
from ..schemas.chat import ChatMessageCreate, ChatMessageResponse
from .deps import get_current_user

router = APIRouter()


async def verify_chronicle_access(db: AsyncSession, chronicle_id: str, user_id: str) -> Chronicle:
    """Verify user has access to chronicle"""
    result = await db.execute(
        select(Chronicle)
        .where(Chronicle.id == chronicle_id)
        .options(selectinload(Chronicle.members))
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Cronica nao encontrada")

    is_storyteller = chronicle.storyteller_id == user_id
    is_member = any(m.user_id == user_id for m in chronicle.members)

    if not is_storyteller and not is_member:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return chronicle


@router.get("/chronicle/{chronicle_id}")
async def get_chat_history(
    chronicle_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get chat history for a chronicle (paginated)"""
    await verify_chronicle_access(db, chronicle_id, current_user.id)

    query = (
        select(ChatMessage)
        .where(ChatMessage.chronicle_id == chronicle_id)
        .where(
            or_(
                ChatMessage.message_type != "whisper",
                ChatMessage.user_id == current_user.id,
                ChatMessage.recipient_id == current_user.id
            )
        )
    )

    if session_id:
        query = query.where(ChatMessage.session_id == session_id)

    query = query.order_by(ChatMessage.created_at.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    messages = result.scalars().all()

    return [
        {
            "id": m.id,
            "chronicle_id": m.chronicle_id,
            "session_id": m.session_id,
            "user_id": m.user_id,
            "character_id": m.character_id,
            "message_type": m.message_type,
            "content": m.content,
            "recipient_id": m.recipient_id,
            "sender_name": m.sender_name,
            "character_name": m.character_name,
            "created_at": m.created_at,
        }
        for m in reversed(messages)  # Return in chronological order
    ]


@router.get("/chronicle/{chronicle_id}/recent")
async def get_recent_messages(
    chronicle_id: str,
    count: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get recent messages for a chronicle"""
    await verify_chronicle_access(db, chronicle_id, current_user.id)

    # Get active session if any
    session_result = await db.execute(
        select(GameSession)
        .where(GameSession.chronicle_id == chronicle_id)
        .where(GameSession.is_active == True)
    )
    active_session = session_result.scalar_one_or_none()

    query = (
        select(ChatMessage)
        .where(ChatMessage.chronicle_id == chronicle_id)
        .where(
            or_(
                ChatMessage.message_type != "whisper",
                ChatMessage.user_id == current_user.id,
                ChatMessage.recipient_id == current_user.id
            )
        )
    )

    # If there's an active session, prefer messages from it
    if active_session:
        query = query.where(
            or_(
                ChatMessage.session_id == active_session.id,
                ChatMessage.session_id == None
            )
        )

    query = query.order_by(ChatMessage.created_at.desc()).limit(count)

    result = await db.execute(query)
    messages = result.scalars().all()

    return [
        {
            "id": m.id,
            "chronicle_id": m.chronicle_id,
            "session_id": m.session_id,
            "user_id": m.user_id,
            "character_id": m.character_id,
            "message_type": m.message_type,
            "content": m.content,
            "recipient_id": m.recipient_id,
            "sender_name": m.sender_name,
            "character_name": m.character_name,
            "created_at": m.created_at,
        }
        for m in reversed(messages)
    ]


@router.post("/chronicle/{chronicle_id}")
async def send_message(
    chronicle_id: str,
    data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a chat message (REST fallback, prefer WebSocket)"""
    chronicle = await verify_chronicle_access(db, chronicle_id, current_user.id)

    # Get character name if character_id provided
    character_name = None
    if data.character_id:
        result = await db.execute(
            select(Character).where(Character.id == data.character_id)
        )
        character = result.scalar_one_or_none()
        if character and character.owner_id == current_user.id:
            character_name = character.name

    # Get active session
    session_result = await db.execute(
        select(GameSession)
        .where(GameSession.chronicle_id == chronicle_id)
        .where(GameSession.is_active == True)
    )
    active_session = session_result.scalar_one_or_none()

    # Create message
    message = ChatMessage(
        id=str(uuid.uuid4()),
        chronicle_id=chronicle_id,
        session_id=active_session.id if active_session else None,
        user_id=current_user.id,
        character_id=data.character_id,
        message_type=data.message_type,
        content=data.content,
        recipient_id=data.recipient_id,
        sender_name=current_user.username,
        character_name=character_name,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    return {
        "id": message.id,
        "chronicle_id": message.chronicle_id,
        "session_id": message.session_id,
        "user_id": message.user_id,
        "character_id": message.character_id,
        "message_type": message.message_type,
        "content": message.content,
        "recipient_id": message.recipient_id,
        "sender_name": message.sender_name,
        "character_name": message.character_name,
        "created_at": message.created_at,
    }
