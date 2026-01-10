from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified
from typing import List
from datetime import datetime
import uuid
import copy

from ..database import get_db
from ..models.xp_request import XPRequest
from ..models.xp_log import XPLog
from ..models.character import Character
from ..models.chronicle import Chronicle, ChronicleMember
from ..models.user import User
from ..schemas.xp import (
    XPRequestCreate, XPRequestResponse, XPApproveRequest,
    XPRejectRequest, XPAwardRequest, XPLogResponse
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


@router.post("/requests", status_code=status.HTTP_201_CREATED)
async def create_xp_request(
    data: XPRequestCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new XP expenditure request"""
    # Get character and verify ownership
    result = await db.execute(
        select(Character)
        .where(Character.id == data.character_id)
        .options(selectinload(Character.chronicle))
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Voce nao e dono deste personagem")

    if not character.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem nao esta em uma cronica")

    # Check if there's already a pending request for the same trait
    existing = await db.execute(
        select(XPRequest)
        .where(XPRequest.character_id == data.character_id)
        .where(XPRequest.trait_type == data.trait_type)
        .where(XPRequest.trait_name == data.trait_name)
        .where(XPRequest.status == "pending")
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Ja existe uma solicitacao pendente para este trait"
        )

    # Create request
    xp_request = XPRequest(
        id=str(uuid.uuid4()),
        chronicle_id=character.chronicle_id,
        character_id=data.character_id,
        requester_id=current_user.id,
        trait_type=data.trait_type,
        trait_name=data.trait_name,
        trait_category=data.trait_category,
        current_value=data.current_value,
        requested_value=data.requested_value,
        xp_cost=data.xp_cost,
        justification=data.justification,
        status="pending",
    )
    db.add(xp_request)
    await db.commit()
    await db.refresh(xp_request)

    return {
        "id": xp_request.id,
        "chronicle_id": xp_request.chronicle_id,
        "character_id": xp_request.character_id,
        "character_name": character.name,
        "trait_type": xp_request.trait_type,
        "trait_name": xp_request.trait_name,
        "xp_cost": xp_request.xp_cost,
        "status": xp_request.status,
        "created_at": xp_request.created_at,
    }


@router.get("/requests/chronicle/{chronicle_id}")
async def list_chronicle_xp_requests(
    chronicle_id: str,
    status_filter: str = "pending",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List XP requests for a chronicle (storyteller sees all, players see own)"""
    # Verify access
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

    if not is_member and not is_storyteller:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # Build query
    query = (
        select(XPRequest)
        .where(XPRequest.chronicle_id == chronicle_id)
        .options(
            selectinload(XPRequest.character),
            selectinload(XPRequest.requester)
        )
    )

    if status_filter != "all":
        query = query.where(XPRequest.status == status_filter)

    # Players only see their own requests
    if not is_storyteller:
        query = query.where(XPRequest.requester_id == current_user.id)

    query = query.order_by(XPRequest.created_at.desc())
    result = await db.execute(query)
    requests = result.scalars().all()

    return [
        {
            "id": r.id,
            "chronicle_id": r.chronicle_id,
            "character_id": r.character_id,
            "character_name": r.character.name if r.character else "Desconhecido",
            "requester_id": r.requester_id,
            "requester_name": r.requester.username if r.requester else "Desconhecido",
            "trait_type": r.trait_type,
            "trait_name": r.trait_name,
            "trait_category": r.trait_category,
            "current_value": r.current_value,
            "requested_value": r.requested_value,
            "xp_cost": r.xp_cost,
            "justification": r.justification,
            "status": r.status,
            "storyteller_message": r.storyteller_message,
            "reviewed_at": r.reviewed_at,
            "created_at": r.created_at,
        }
        for r in requests
    ]


@router.get("/requests/character/{character_id}")
async def list_character_xp_requests(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List XP requests for a specific character"""
    # Verify access
    result = await db.execute(
        select(Character).where(Character.id == character_id)
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if character.owner_id != current_user.id:
        # Check if storyteller
        if character.chronicle_id:
            storyteller_id = await get_chronicle_storyteller(db, character.chronicle_id)
            if storyteller_id != current_user.id:
                raise HTTPException(status_code=403, detail="Acesso negado")
        else:
            raise HTTPException(status_code=403, detail="Acesso negado")

    result = await db.execute(
        select(XPRequest)
        .where(XPRequest.character_id == character_id)
        .order_by(XPRequest.created_at.desc())
    )
    requests = result.scalars().all()

    return [
        {
            "id": r.id,
            "trait_type": r.trait_type,
            "trait_name": r.trait_name,
            "current_value": r.current_value,
            "requested_value": r.requested_value,
            "xp_cost": r.xp_cost,
            "status": r.status,
            "storyteller_message": r.storyteller_message,
            "created_at": r.created_at,
        }
        for r in requests
    ]


@router.post("/requests/{request_id}/approve")
async def approve_xp_request(
    request_id: str,
    data: XPApproveRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Approve an XP request (storyteller only)"""
    result = await db.execute(
        select(XPRequest)
        .where(XPRequest.id == request_id)
        .options(selectinload(XPRequest.character))
    )
    xp_request = result.scalar_one_or_none()

    if not xp_request:
        raise HTTPException(status_code=404, detail="Solicitacao nao encontrada")

    if xp_request.status != "pending":
        raise HTTPException(status_code=400, detail="Solicitacao ja foi processada")

    await verify_storyteller(db, xp_request.chronicle_id, current_user.id)

    character = xp_request.character
    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    # Get current XP from character sheet
    sheet = dict(character.sheet) if character.sheet else {}
    # Support both Portuguese and English keys
    experience = dict(sheet.get("experiencia", sheet.get("experience", {"total": 0, "gasta": 0})))
    current_total = experience.get("total", 0)
    current_spent = experience.get("gasta", experience.get("spent", 0))
    available_xp = current_total - current_spent

    if available_xp < xp_request.xp_cost:
        raise HTTPException(
            status_code=400,
            detail=f"XP insuficiente. Disponivel: {available_xp}, Custo: {xp_request.xp_cost}"
        )

    # Update XP
    new_spent = current_spent + xp_request.xp_cost
    # Preserve key style
    if "experiencia" in sheet:
        sheet["experiencia"] = {"total": current_total, "gasta": new_spent}
    else:
        sheet["experience"] = {"total": current_total, "spent": new_spent}

    # Update trait value in sheet
    trait_updated = update_trait_in_sheet(
        sheet,
        xp_request.trait_type,
        xp_request.trait_name,
        xp_request.trait_category,
        xp_request.requested_value
    )

    character.sheet = sheet
    flag_modified(character, 'sheet')  # Force SQLAlchemy to detect JSON change

    # Update request status
    xp_request.status = "approved"
    xp_request.storyteller_message = data.message
    xp_request.reviewed_by_id = current_user.id
    xp_request.reviewed_at = datetime.utcnow()

    # Create XP log
    xp_log = XPLog(
        id=str(uuid.uuid4()),
        character_id=character.id,
        chronicle_id=xp_request.chronicle_id,
        change_type="spend",
        amount=-xp_request.xp_cost,
        previous_total=available_xp,
        new_total=available_xp - xp_request.xp_cost,
        description=f"Gasto em {xp_request.trait_name} ({xp_request.current_value} -> {xp_request.requested_value})",
        trait_affected=xp_request.trait_name,
        xp_request_id=xp_request.id,
        performed_by_id=current_user.id,
    )
    db.add(xp_log)

    await db.commit()

    return {
        "message": "Solicitacao aprovada",
        "request_id": xp_request.id,
        "trait_name": xp_request.trait_name,
        "new_value": xp_request.requested_value,
        "xp_spent": xp_request.xp_cost,
    }


@router.post("/requests/{request_id}/reject")
async def reject_xp_request(
    request_id: str,
    data: XPRejectRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reject an XP request (storyteller only)"""
    result = await db.execute(
        select(XPRequest).where(XPRequest.id == request_id)
    )
    xp_request = result.scalar_one_or_none()

    if not xp_request:
        raise HTTPException(status_code=404, detail="Solicitacao nao encontrada")

    if xp_request.status != "pending":
        raise HTTPException(status_code=400, detail="Solicitacao ja foi processada")

    await verify_storyteller(db, xp_request.chronicle_id, current_user.id)

    xp_request.status = "rejected"
    xp_request.storyteller_message = data.message
    xp_request.reviewed_by_id = current_user.id
    xp_request.reviewed_at = datetime.utcnow()

    await db.commit()

    return {
        "message": "Solicitacao rejeitada",
        "request_id": xp_request.id,
    }


@router.get("/logs/character/{character_id}")
async def get_character_xp_logs(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get XP history for a character"""
    result = await db.execute(
        select(Character).where(Character.id == character_id)
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    # Verify access
    if character.owner_id != current_user.id:
        if character.chronicle_id:
            storyteller_id = await get_chronicle_storyteller(db, character.chronicle_id)
            if storyteller_id != current_user.id:
                raise HTTPException(status_code=403, detail="Acesso negado")
        else:
            raise HTTPException(status_code=403, detail="Acesso negado")

    result = await db.execute(
        select(XPLog)
        .where(XPLog.character_id == character_id)
        .options(selectinload(XPLog.performed_by))
        .order_by(XPLog.created_at.desc())
    )
    logs = result.scalars().all()

    return [
        {
            "id": log.id,
            "change_type": log.change_type,
            "amount": log.amount,
            "previous_total": log.previous_total,
            "new_total": log.new_total,
            "description": log.description,
            "trait_affected": log.trait_affected,
            "performed_by_name": log.performed_by.username if log.performed_by else "Sistema",
            "created_at": log.created_at,
        }
        for log in logs
    ]


@router.post("/award")
async def award_xp(
    data: XPAwardRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Award XP to a character (storyteller only)"""
    result = await db.execute(
        select(Character).where(Character.id == data.character_id)
    )
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if not character.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem nao esta em uma cronica")

    await verify_storyteller(db, character.chronicle_id, current_user.id)

    # Update XP in sheet - make a deep copy to ensure SQLAlchemy detects the change
    sheet = copy.deepcopy(character.sheet) if character.sheet else {}
    # Support both Portuguese (experiencia) and English (experience) keys
    experience_key = "experiencia" if "experiencia" in sheet else "experience"
    experience = dict(sheet.get(experience_key, {"total": 0, "gasta": 0}))
    old_total = experience.get("total", 0)
    new_total = old_total + data.amount
    experience["total"] = new_total
    sheet[experience_key] = experience
    # Force SQLAlchemy to detect the change by setting to None first, then new value
    character.sheet = None
    await db.flush()
    character.sheet = sheet
    flag_modified(character, 'sheet')

    # Create log
    xp_log = XPLog(
        id=str(uuid.uuid4()),
        character_id=character.id,
        chronicle_id=character.chronicle_id,
        session_id=data.session_id,
        change_type="award",
        amount=data.amount,
        previous_total=old_total,
        new_total=new_total,
        description=data.description,
        performed_by_id=current_user.id,
    )
    db.add(xp_log)

    await db.commit()

    return {
        "message": f"{data.amount} XP concedido",
        "character_id": character.id,
        "character_name": character.name,
        "new_total": new_total,
    }


def update_trait_in_sheet(
    sheet: dict,
    trait_type: str,
    trait_name: str,
    trait_category: str,
    new_value: int
) -> bool:
    """Update a trait value in the character sheet"""
    try:
        if trait_type == "attribute":
            if trait_category and trait_category in sheet.get("attributes", {}):
                sheet["attributes"][trait_category][trait_name] = new_value
                return True
        elif trait_type == "skill":
            if trait_category and trait_category in sheet.get("skills", {}):
                sheet["skills"][trait_category][trait_name] = new_value
                return True
        elif trait_type == "discipline":
            if "disciplines" not in sheet:
                sheet["disciplines"] = {}
            sheet["disciplines"][trait_name] = new_value
            return True
        elif trait_type == "background":
            if "backgrounds" not in sheet:
                sheet["backgrounds"] = {}
            sheet["backgrounds"][trait_name] = new_value
            return True
        elif trait_type == "ability":
            if trait_category and trait_category in sheet.get("abilities", {}):
                sheet["abilities"][trait_category][trait_name] = new_value
                return True
        elif trait_type == "blood_potency":
            sheet["blood_potency"] = new_value
            return True
        elif trait_type == "humanity":
            sheet["humanity"] = new_value
            return True

        return False
    except Exception:
        return False
