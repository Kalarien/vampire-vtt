from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified
from typing import Optional
from datetime import datetime
import uuid

from ..database import get_db
from ..models.game_session import GameSession
from ..models.session_participant import SessionParticipant
from ..models.chronicle import Chronicle, ChronicleMember
from ..models.character import Character
from ..models.xp_log import XPLog
from ..models.user import User
from ..schemas.session import (
    SessionStart, SessionEnd, SessionJoin,
    SessionResponse, SessionListResponse, SessionParticipantResponse
)
from .deps import get_current_user

router = APIRouter()


async def get_chronicle_storyteller(db: AsyncSession, chronicle_id: str) -> str:
    """Get storyteller ID for a chronicle"""
    result = await db.execute(
        select(Chronicle).where(Chronicle.id == chronicle_id)
    )
    chronicle = result.scalar_one_or_none()
    if not chronicle:
        raise HTTPException(status_code=404, detail="Cronica nao encontrada")
    return chronicle.storyteller_id


async def verify_storyteller(db: AsyncSession, chronicle_id: str, user_id: str):
    """Verify user is storyteller of chronicle"""
    storyteller_id = await get_chronicle_storyteller(db, chronicle_id)
    if storyteller_id != user_id:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode fazer isso")


async def verify_chronicle_member(db: AsyncSession, chronicle_id: str, user_id: str) -> bool:
    """Check if user is member of chronicle"""
    result = await db.execute(
        select(ChronicleMember)
        .where(ChronicleMember.chronicle_id == chronicle_id)
        .where(ChronicleMember.user_id == user_id)
    )
    return result.scalar_one_or_none() is not None


@router.post("/chronicle/{chronicle_id}/start", status_code=status.HTTP_201_CREATED)
async def start_session(
    chronicle_id: str,
    data: SessionStart,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start a new game session (storyteller only)"""
    await verify_storyteller(db, chronicle_id, current_user.id)

    # Check if there's already an active session
    result = await db.execute(
        select(GameSession)
        .where(GameSession.chronicle_id == chronicle_id)
        .where(GameSession.is_active == True)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Ja existe uma sessao ativa nesta cronica"
        )

    # Get next session number
    result = await db.execute(
        select(func.max(GameSession.number))
        .where(GameSession.chronicle_id == chronicle_id)
    )
    max_number = result.scalar() or 0
    next_number = max_number + 1

    # Create session
    session = GameSession(
        id=str(uuid.uuid4()),
        chronicle_id=chronicle_id,
        name=data.name or f"Sessao {next_number}",
        number=next_number,
        notes=data.notes,
        is_active=True,
        started_by_id=current_user.id,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {
        "id": session.id,
        "chronicle_id": session.chronicle_id,
        "name": session.name,
        "number": session.number,
        "started_at": session.started_at,
        "is_active": session.is_active,
        "message": "Sessao iniciada!"
    }


@router.post("/{session_id}/end")
async def end_session(
    session_id: str,
    data: SessionEnd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """End a game session and optionally award XP (storyteller only)"""
    result = await db.execute(
        select(GameSession)
        .where(GameSession.id == session_id)
        .options(selectinload(GameSession.participants).selectinload(SessionParticipant.character))
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")

    if not session.is_active:
        raise HTTPException(status_code=400, detail="Sessao ja foi encerrada")

    await verify_storyteller(db, session.chronicle_id, current_user.id)

    # End the session
    session.is_active = False
    session.ended_at = datetime.utcnow()
    session.notes = data.notes or session.notes
    session.xp_awarded = data.xp_amount

    # Award XP to all participants
    if data.xp_amount > 0:
        for participant in session.participants:
            if participant.left_at is None:  # Still in session
                character = participant.character
                if character:
                    # Update character XP
                    sheet = dict(character.sheet) if character.sheet else {}
                    experience = dict(sheet.get("experiencia", sheet.get("experience", {"total": 0, "gasta": 0})))
                    old_total = experience.get("total", 0)
                    new_total = old_total + data.xp_amount
                    experience["total"] = new_total
                    # Support both Portuguese and English keys
                    if "experiencia" in sheet:
                        sheet["experiencia"] = experience
                    else:
                        sheet["experience"] = experience
                    character.sheet = sheet
                    flag_modified(character, 'sheet')  # Force SQLAlchemy to detect change

                    # Update participant record
                    participant.xp_received = data.xp_amount

                    # Create XP log
                    xp_log = XPLog(
                        id=str(uuid.uuid4()),
                        character_id=character.id,
                        chronicle_id=session.chronicle_id,
                        session_id=session.id,
                        change_type="award",
                        amount=data.xp_amount,
                        previous_total=old_total,
                        new_total=new_total,
                        description=data.xp_description,
                        performed_by_id=current_user.id,
                    )
                    db.add(xp_log)

    await db.commit()

    return {
        "message": "Sessao encerrada",
        "session_id": session.id,
        "xp_awarded": data.xp_amount,
        "participants_count": len([p for p in session.participants if p.left_at is None])
    }


@router.get("/chronicle/{chronicle_id}")
async def list_sessions(
    chronicle_id: str,
    active_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all sessions for a chronicle"""
    # Verify access
    storyteller_id = await get_chronicle_storyteller(db, chronicle_id)
    is_storyteller = storyteller_id == current_user.id
    is_member = await verify_chronicle_member(db, chronicle_id, current_user.id)

    if not is_storyteller and not is_member:
        raise HTTPException(status_code=403, detail="Acesso negado")

    query = (
        select(GameSession)
        .where(GameSession.chronicle_id == chronicle_id)
        .options(selectinload(GameSession.participants))
        .order_by(GameSession.started_at.desc())
    )

    if active_only:
        query = query.where(GameSession.is_active == True)

    result = await db.execute(query)
    sessions = result.scalars().all()

    return [
        {
            "id": s.id,
            "chronicle_id": s.chronicle_id,
            "name": s.name,
            "number": s.number,
            "started_at": s.started_at,
            "ended_at": s.ended_at,
            "is_active": s.is_active,
            "xp_awarded": s.xp_awarded,
            "participant_count": len(s.participants)
        }
        for s in sessions
    ]


@router.get("/chronicle/{chronicle_id}/active")
async def get_active_session(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the active session for a chronicle"""
    # Verify access
    storyteller_id = await get_chronicle_storyteller(db, chronicle_id)
    is_storyteller = storyteller_id == current_user.id
    is_member = await verify_chronicle_member(db, chronicle_id, current_user.id)

    if not is_storyteller and not is_member:
        raise HTTPException(status_code=403, detail="Acesso negado")

    result = await db.execute(
        select(GameSession)
        .where(GameSession.chronicle_id == chronicle_id)
        .where(GameSession.is_active == True)
        .options(
            selectinload(GameSession.participants).selectinload(SessionParticipant.character),
            selectinload(GameSession.participants).selectinload(SessionParticipant.user),
            selectinload(GameSession.started_by)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        return None

    return {
        "id": session.id,
        "chronicle_id": session.chronicle_id,
        "name": session.name,
        "number": session.number,
        "notes": session.notes,
        "started_at": session.started_at,
        "is_active": session.is_active,
        "active_scene_id": session.active_scene_id,
        "started_by_id": session.started_by_id,
        "started_by_name": session.started_by.username if session.started_by else "Desconhecido",
        "participants": [
            {
                "id": p.id,
                "character_id": p.character_id,
                "character_name": p.character.name if p.character else "Desconhecido",
                "user_id": p.user_id,
                "username": p.user.username if p.user else "Desconhecido",
                "joined_at": p.joined_at,
                "left_at": p.left_at,
                "xp_received": p.xp_received or 0
            }
            for p in session.participants
        ]
    }


@router.get("/{session_id}")
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get session details"""
    result = await db.execute(
        select(GameSession)
        .where(GameSession.id == session_id)
        .options(
            selectinload(GameSession.participants).selectinload(SessionParticipant.character),
            selectinload(GameSession.participants).selectinload(SessionParticipant.user),
            selectinload(GameSession.started_by)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")

    # Verify access
    storyteller_id = await get_chronicle_storyteller(db, session.chronicle_id)
    is_storyteller = storyteller_id == current_user.id
    is_member = await verify_chronicle_member(db, session.chronicle_id, current_user.id)

    if not is_storyteller and not is_member:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return {
        "id": session.id,
        "chronicle_id": session.chronicle_id,
        "name": session.name,
        "number": session.number,
        "notes": session.notes,
        "started_at": session.started_at,
        "ended_at": session.ended_at,
        "is_active": session.is_active,
        "active_scene_id": session.active_scene_id,
        "xp_awarded": session.xp_awarded,
        "started_by_id": session.started_by_id,
        "started_by_name": session.started_by.username if session.started_by else "Desconhecido",
        "participants": [
            {
                "id": p.id,
                "character_id": p.character_id,
                "character_name": p.character.name if p.character else "Desconhecido",
                "user_id": p.user_id,
                "username": p.user.username if p.user else "Desconhecido",
                "joined_at": p.joined_at,
                "left_at": p.left_at,
                "xp_received": p.xp_received or 0
            }
            for p in session.participants
        ]
    }


@router.post("/{session_id}/join")
async def join_session(
    session_id: str,
    data: SessionJoin,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Join a session with a character"""
    result = await db.execute(
        select(GameSession).where(GameSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")

    if not session.is_active:
        raise HTTPException(status_code=400, detail="Sessao nao esta ativa")

    # Verify character exists and belongs to chronicle
    result = await db.execute(
        select(Character).where(Character.id == data.character_id)
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if character.chronicle_id != session.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem nao pertence a esta cronica")

    # Check if user is owner or storyteller
    chronicle_result = await db.execute(
        select(Chronicle).where(Chronicle.id == session.chronicle_id)
    )
    chronicle = chronicle_result.scalar_one_or_none()
    is_storyteller = chronicle and chronicle.storyteller_id == current_user.id
    is_owner = character.owner_id == current_user.id

    if not is_owner and not is_storyteller:
        raise HTTPException(status_code=403, detail="Apenas o dono do personagem ou o Narrador podem adicionar a sessao")

    # Check if already in session
    result = await db.execute(
        select(SessionParticipant)
        .where(SessionParticipant.session_id == session_id)
        .where(SessionParticipant.character_id == data.character_id)
        .where(SessionParticipant.left_at == None)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Personagem ja esta na sessao")

    # Add participant (use character owner's id, not current user if storyteller is adding)
    participant = SessionParticipant(
        id=str(uuid.uuid4()),
        session_id=session_id,
        character_id=data.character_id,
        user_id=character.owner_id,
    )
    db.add(participant)
    await db.commit()

    added_by = "Narrador" if is_storyteller and not is_owner else "Jogador"
    return {
        "message": f"Personagem adicionado a sessao pelo {added_by}",
        "session_id": session_id,
        "character_id": data.character_id,
        "character_name": character.name
    }


@router.post("/{session_id}/leave")
async def leave_session(
    session_id: str,
    data: SessionJoin,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Leave a session"""
    result = await db.execute(
        select(SessionParticipant)
        .where(SessionParticipant.session_id == session_id)
        .where(SessionParticipant.character_id == data.character_id)
        .where(SessionParticipant.left_at == None)
    )
    participant = result.scalar_one_or_none()

    if not participant:
        raise HTTPException(status_code=404, detail="Participante nao encontrado")

    if participant.user_id != current_user.id:
        # Check if storyteller
        result = await db.execute(
            select(GameSession).where(GameSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if session:
            storyteller_id = await get_chronicle_storyteller(db, session.chronicle_id)
            if storyteller_id != current_user.id:
                raise HTTPException(status_code=403, detail="Acesso negado")

    participant.left_at = datetime.utcnow()
    await db.commit()

    return {
        "message": "Saiu da sessao",
        "session_id": session_id,
        "character_id": data.character_id
    }


@router.post("/{session_id}/scene/{scene_id}")
async def set_active_scene(
    session_id: str,
    scene_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set the active scene for a session (storyteller only)"""
    result = await db.execute(
        select(GameSession).where(GameSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")

    await verify_storyteller(db, session.chronicle_id, current_user.id)

    session.active_scene_id = scene_id
    await db.commit()

    return {
        "message": "Cena ativa definida",
        "session_id": session_id,
        "scene_id": scene_id
    }
