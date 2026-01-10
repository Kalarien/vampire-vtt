from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime
import uuid
import random

from ..database import get_db
from ..models.initiative import InitiativeOrder, InitiativeEntry
from ..models.game_session import GameSession
from ..models.chronicle import Chronicle
from ..models.character import Character
from ..models.user import User
from ..schemas.initiative import (
    InitiativeStart, InitiativeEntryAdd, InitiativeEntryUpdate,
    InitiativeOrderResponse, InitiativeEntryResponse
)
from .deps import get_current_user

router = APIRouter()


async def get_session_chronicle(db: AsyncSession, session_id: str) -> tuple:
    """Get session and chronicle for verification"""
    result = await db.execute(
        select(GameSession).where(GameSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")

    result = await db.execute(
        select(Chronicle).where(Chronicle.id == session.chronicle_id)
    )
    chronicle = result.scalar_one_or_none()
    return session, chronicle


async def verify_storyteller(db: AsyncSession, session_id: str, user_id: str):
    """Verify user is storyteller of session's chronicle"""
    session, chronicle = await get_session_chronicle(db, session_id)
    if not chronicle or chronicle.storyteller_id != user_id:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode fazer isso")
    return session


def format_order_response(order: InitiativeOrder, entries: list) -> dict:
    """Format initiative order response"""
    sorted_entries = sorted(entries, key=lambda e: e.initiative_value, reverse=True)
    return {
        "id": order.id,
        "session_id": order.session_id,
        "name": order.name,
        "is_active": order.is_active,
        "current_round": order.current_round,
        "current_turn_index": order.current_turn_index,
        "entries": [
            {
                "id": e.id,
                "order_id": e.order_id,
                "character_id": e.character_id,
                "character_name": e.character_name,
                "initiative_value": e.initiative_value,
                "initiative_modifier": e.initiative_modifier,
                "is_npc": e.is_npc,
                "has_acted": e.has_acted,
                "is_delayed": e.is_delayed,
                "created_at": e.created_at,
            }
            for e in sorted_entries
        ],
        "created_at": order.created_at,
        "ended_at": order.ended_at,
    }


@router.post("/session/{session_id}/start", status_code=status.HTTP_201_CREATED)
async def start_combat(
    session_id: str,
    data: InitiativeStart,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start a new initiative/combat order (storyteller only)"""
    session = await verify_storyteller(db, session_id, current_user.id)

    if not session.is_active:
        raise HTTPException(status_code=400, detail="Sessao nao esta ativa")

    # Check if there's already an active initiative
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.session_id == session_id)
        .where(InitiativeOrder.is_active == True)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ja existe um combate ativo")

    # Create initiative order
    order = InitiativeOrder(
        id=str(uuid.uuid4()),
        session_id=session_id,
        name=data.name or "Combate",
        is_active=True,
        current_round=1,
        current_turn_index=0,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return format_order_response(order, [])


@router.get("/session/{session_id}")
async def get_current_initiative(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current active initiative for a session"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.session_id == session_id)
        .where(InitiativeOrder.is_active == True)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        return None

    return format_order_response(order, order.entries)


@router.get("/{order_id}")
async def get_initiative_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get initiative order by ID"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    return format_order_response(order, order.entries)


@router.post("/{order_id}/add")
async def add_to_initiative(
    order_id: str,
    data: InitiativeEntryAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add character/NPC to initiative (storyteller only)"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    await verify_storyteller(db, order.session_id, current_user.id)

    if not order.is_active:
        raise HTTPException(status_code=400, detail="Combate ja encerrado")

    # Create entry
    entry = InitiativeEntry(
        id=str(uuid.uuid4()),
        order_id=order_id,
        character_id=data.character_id,
        character_name=data.character_name,
        initiative_value=data.initiative_value,
        initiative_modifier=data.initiative_modifier,
        is_npc=data.is_npc,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    # Refresh order entries
    await db.refresh(order)

    return format_order_response(order, order.entries)


@router.delete("/{order_id}/remove/{entry_id}")
async def remove_from_initiative(
    order_id: str,
    entry_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove entry from initiative (storyteller only)"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    await verify_storyteller(db, order.session_id, current_user.id)

    # Find and remove entry
    result = await db.execute(
        select(InitiativeEntry)
        .where(InitiativeEntry.id == entry_id)
        .where(InitiativeEntry.order_id == order_id)
    )
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Entrada nao encontrada")

    await db.delete(entry)
    await db.commit()

    # Refresh order
    await db.refresh(order)

    return format_order_response(order, order.entries)


@router.patch("/{order_id}/entry/{entry_id}")
async def update_initiative_entry(
    order_id: str,
    entry_id: str,
    data: InitiativeEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an initiative entry (storyteller only)"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    await verify_storyteller(db, order.session_id, current_user.id)

    # Find entry
    result = await db.execute(
        select(InitiativeEntry)
        .where(InitiativeEntry.id == entry_id)
        .where(InitiativeEntry.order_id == order_id)
    )
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Entrada nao encontrada")

    if data.initiative_value is not None:
        entry.initiative_value = data.initiative_value
    if data.has_acted is not None:
        entry.has_acted = data.has_acted
    if data.is_delayed is not None:
        entry.is_delayed = data.is_delayed

    await db.commit()
    await db.refresh(order)

    return format_order_response(order, order.entries)


@router.post("/{order_id}/roll")
async def roll_all_initiative(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Roll initiative for all entries (storyteller only)"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    await verify_storyteller(db, order.session_id, current_user.id)

    # Roll for each entry: 1d10 + modifier
    for entry in order.entries:
        roll = random.randint(1, 10)
        entry.initiative_value = roll + entry.initiative_modifier
        entry.has_acted = False

    await db.commit()
    await db.refresh(order)

    return format_order_response(order, order.entries)


@router.post("/{order_id}/next")
async def next_turn(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Advance to next turn (storyteller only)"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    await verify_storyteller(db, order.session_id, current_user.id)

    if not order.is_active:
        raise HTTPException(status_code=400, detail="Combate ja encerrado")

    sorted_entries = sorted(order.entries, key=lambda e: e.initiative_value, reverse=True)

    if not sorted_entries:
        raise HTTPException(status_code=400, detail="Nenhum participante no combate")

    # Mark current as acted
    if order.current_turn_index < len(sorted_entries):
        sorted_entries[order.current_turn_index].has_acted = True

    # Move to next
    order.current_turn_index += 1

    # Check if round ended
    if order.current_turn_index >= len(sorted_entries):
        order.current_round += 1
        order.current_turn_index = 0
        # Reset has_acted for new round
        for entry in order.entries:
            entry.has_acted = False

    await db.commit()
    await db.refresh(order)

    return format_order_response(order, order.entries)


@router.post("/{order_id}/end")
async def end_combat(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """End combat (storyteller only)"""
    result = await db.execute(
        select(InitiativeOrder)
        .where(InitiativeOrder.id == order_id)
        .options(selectinload(InitiativeOrder.entries))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Ordem de iniciativa nao encontrada")

    await verify_storyteller(db, order.session_id, current_user.id)

    order.is_active = False
    order.ended_at = datetime.utcnow()

    await db.commit()
    await db.refresh(order)

    return {
        "message": "Combate encerrado",
        "order_id": order.id,
        "rounds": order.current_round
    }
