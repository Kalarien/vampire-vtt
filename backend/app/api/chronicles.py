from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models.chronicle import Chronicle, ChronicleMember
from ..models.character import Character
from ..models.scene import Scene
from ..models.user import User
from .deps import get_current_user

router = APIRouter()


# Schemas
class ChronicleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    game_version: str = "v5"  # "v5" or "v20"


class ChronicleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ChronicleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    game_version: str
    storyteller_id: str
    invite_code: str
    is_active: bool
    member_count: int = 0

    class Config:
        from_attributes = True


class ChronicleDetailResponse(ChronicleResponse):
    storyteller_username: Optional[str] = None
    members: List[dict] = []


@router.get("/")
async def list_chronicles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all chronicles where user is storyteller or member"""
    # Get chronicles where user is storyteller
    storyteller_result = await db.execute(
        select(Chronicle)
        .where(Chronicle.storyteller_id == current_user.id)
        .options(selectinload(Chronicle.members))
    )
    storyteller_chronicles = storyteller_result.scalars().all()

    # Get chronicles where user is a member
    member_result = await db.execute(
        select(Chronicle)
        .join(ChronicleMember)
        .where(ChronicleMember.user_id == current_user.id)
        .options(selectinload(Chronicle.members))
    )
    member_chronicles = member_result.scalars().all()

    # Combine and deduplicate
    all_chronicles = {c.id: c for c in storyteller_chronicles}
    for c in member_chronicles:
        if c.id not in all_chronicles:
            all_chronicles[c.id] = c

    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "game_version": c.game_version,
            "storyteller_id": c.storyteller_id,
            "invite_code": c.invite_code,
            "is_active": c.is_active,
            "member_count": len(c.members) if c.members else 0,
        }
        for c in all_chronicles.values()
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chronicle(
    chronicle_data: ChronicleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new chronicle"""
    chronicle = Chronicle(
        id=str(uuid.uuid4()),
        name=chronicle_data.name,
        description=chronicle_data.description,
        game_version=chronicle_data.game_version,
        storyteller_id=current_user.id,
    )
    db.add(chronicle)

    # Add storyteller as member
    member = ChronicleMember(
        id=str(uuid.uuid4()),
        chronicle_id=chronicle.id,
        user_id=current_user.id,
        role="storyteller",
    )
    db.add(member)

    await db.commit()
    await db.refresh(chronicle)

    return {
        "id": chronicle.id,
        "name": chronicle.name,
        "description": chronicle.description,
        "game_version": chronicle.game_version,
        "storyteller_id": chronicle.storyteller_id,
        "invite_code": chronicle.invite_code,
        "is_active": chronicle.is_active,
        "member_count": 1,
    }


@router.get("/{chronicle_id}")
async def get_chronicle(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get chronicle by ID with full details"""
    result = await db.execute(
        select(Chronicle)
        .where(Chronicle.id == chronicle_id)
        .options(
            selectinload(Chronicle.members).selectinload(ChronicleMember.user),
            selectinload(Chronicle.storyteller),
            selectinload(Chronicle.characters).selectinload(Character.owner),
        )
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Chronicle not found")

    # Check if user has access
    is_member = any(m.user_id == current_user.id for m in chronicle.members)
    is_storyteller = chronicle.storyteller_id == current_user.id

    if not is_member and not is_storyteller:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "id": chronicle.id,
        "name": chronicle.name,
        "description": chronicle.description,
        "game_version": chronicle.game_version,
        "storyteller_id": chronicle.storyteller_id,
        "storyteller_username": chronicle.storyteller.username if chronicle.storyteller else None,
        "invite_code": chronicle.invite_code,
        "is_active": chronicle.is_active,
        "created_at": chronicle.created_at.isoformat() if chronicle.created_at else None,
        "member_count": len(chronicle.members),
        "members": [
            {
                "id": m.id,
                "user_id": m.user_id,
                "username": m.user.username if m.user else "Unknown",
                "role": m.role,
            }
            for m in chronicle.members
        ],
        "characters": [
            {
                "id": c.id,
                "name": c.name,
                "clan": c.clan,
                "concept": c.concept,
                "game_version": c.game_version,
                "owner_id": c.owner_id,
                "owner_name": c.owner.username if c.owner else "Desconhecido",
                "approval_status": c.approval_status or "draft",
                "sheet": c.sheet,
            }
            for c in chronicle.characters
        ],
    }


@router.patch("/{chronicle_id}")
async def update_chronicle(
    chronicle_id: str,
    chronicle_data: ChronicleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update chronicle (storyteller only)"""
    result = await db.execute(
        select(Chronicle).where(Chronicle.id == chronicle_id)
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Chronicle not found")

    if chronicle.storyteller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only storyteller can update")

    if chronicle_data.name is not None:
        chronicle.name = chronicle_data.name
    if chronicle_data.description is not None:
        chronicle.description = chronicle_data.description

    await db.commit()
    await db.refresh(chronicle)

    return {
        "id": chronicle.id,
        "name": chronicle.name,
        "description": chronicle.description,
        "game_version": chronicle.game_version,
        "storyteller_id": chronicle.storyteller_id,
        "invite_code": chronicle.invite_code,
        "is_active": chronicle.is_active,
    }


@router.delete("/{chronicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chronicle(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete chronicle (storyteller only)"""
    result = await db.execute(
        select(Chronicle).where(Chronicle.id == chronicle_id)
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Chronicle not found")

    if chronicle.storyteller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only storyteller can delete")

    await db.delete(chronicle)
    await db.commit()


@router.post("/join/{invite_code}")
async def join_chronicle(
    invite_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Join chronicle by invite code"""
    result = await db.execute(
        select(Chronicle)
        .where(Chronicle.invite_code == invite_code)
        .options(selectinload(Chronicle.members))
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Codigo de convite invalido")

    if not chronicle.is_active:
        raise HTTPException(status_code=400, detail="Esta cronica nao esta ativa")

    # Check if already a member
    is_member = any(m.user_id == current_user.id for m in chronicle.members)
    if is_member:
        raise HTTPException(status_code=400, detail="Voce ja e membro desta cronica")

    # Add as player
    member = ChronicleMember(
        id=str(uuid.uuid4()),
        chronicle_id=chronicle.id,
        user_id=current_user.id,
        role="player",
    )
    db.add(member)
    await db.commit()

    return {
        "message": "Entrou na cronica com sucesso",
        "chronicle_id": chronicle.id,
        "chronicle_name": chronicle.name,
    }


@router.post("/{chronicle_id}/leave")
async def leave_chronicle(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Leave a chronicle"""
    # Get chronicle
    result = await db.execute(
        select(Chronicle).where(Chronicle.id == chronicle_id)
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Chronicle not found")

    # Storyteller cannot leave
    if chronicle.storyteller_id == current_user.id:
        raise HTTPException(status_code=400, detail="Storyteller cannot leave. Delete the chronicle instead.")

    # Find membership
    member_result = await db.execute(
        select(ChronicleMember)
        .where(ChronicleMember.chronicle_id == chronicle_id)
        .where(ChronicleMember.user_id == current_user.id)
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(status_code=400, detail="Not a member of this chronicle")

    await db.delete(member)
    await db.commit()

    return {"message": "Left chronicle successfully"}


@router.post("/{chronicle_id}/regenerate-invite")
async def regenerate_invite_code(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Regenerate invite code (storyteller only)"""
    import secrets

    result = await db.execute(
        select(Chronicle).where(Chronicle.id == chronicle_id)
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Chronicle not found")

    if chronicle.storyteller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only storyteller can regenerate invite")

    chronicle.invite_code = secrets.token_urlsafe(12)
    await db.commit()
    await db.refresh(chronicle)

    return {"invite_code": chronicle.invite_code}


# ============== SCENES SHORTCUT ==============
@router.get("/{chronicle_id}/scenes")
async def list_chronicle_scenes(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all scenes for a chronicle (shortcut route)"""
    # Verify chronicle access
    result = await db.execute(
        select(Chronicle)
        .where(Chronicle.id == chronicle_id)
        .options(selectinload(Chronicle.members))
    )
    chronicle = result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Cronica nao encontrada")

    is_storyteller = chronicle.storyteller_id == current_user.id
    is_member = any(m.user_id == current_user.id for m in chronicle.members)

    if not is_storyteller and not is_member:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # Get scenes
    result = await db.execute(
        select(Scene)
        .where(Scene.chronicle_id == chronicle_id)
        .order_by(Scene.created_at.desc())
    )
    scenes = result.scalars().all()

    return [
        {
            "id": s.id,
            "chronicle_id": s.chronicle_id,
            "name": s.name,
            "description": s.description,
            "location": s.location,
            "is_active": s.is_active,
            "image_url": s.image_url,
            "created_at": s.created_at,
        }
        for s in scenes
    ]
