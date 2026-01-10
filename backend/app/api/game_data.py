from fastapi import APIRouter

from ..game_data.v5 import (
    CLANS_V5,
    DISCIPLINES_V5,
    PREDATOR_TYPES_V5,
    LORESHEETS_V5,
    BLOOD_POTENCY_TABLE,
    BACKGROUNDS_V5,
    MERITS_V5,
    FLAWS_V5,
    COTERIE_TYPES_V5,
    BLOOD_SORCERY_RITUALS_V5,
)
from ..game_data.v20 import CLANS_V20, DISCIPLINES_V20, BACKGROUNDS_V20

router = APIRouter()


# === V5 Game Data ===

@router.get("/v5/clans")
async def get_v5_clans():
    """Get all V5 clans"""
    return {key: clan.model_dump() for key, clan in CLANS_V5.items()}


@router.get("/v5/clans/{clan_id}")
async def get_v5_clan(clan_id: str):
    """Get a specific V5 clan"""
    clan = CLANS_V5.get(clan_id)
    if not clan:
        return {"error": "Clan not found"}
    return clan.model_dump()


@router.get("/v5/disciplines")
async def get_v5_disciplines():
    """Get all V5 disciplines"""
    return {key: disc.model_dump() for key, disc in DISCIPLINES_V5.items()}


@router.get("/v5/disciplines/{discipline_id}")
async def get_v5_discipline(discipline_id: str):
    """Get a specific V5 discipline"""
    disc = DISCIPLINES_V5.get(discipline_id)
    if not disc:
        return {"error": "Discipline not found"}
    return disc.model_dump()


@router.get("/v5/predator-types")
async def get_v5_predator_types():
    """Get all V5 predator types"""
    return {key: pt.model_dump() for key, pt in PREDATOR_TYPES_V5.items()}


@router.get("/v5/loresheets")
async def get_v5_loresheets():
    """Get all V5 loresheets"""
    return {key: ls.model_dump() for key, ls in LORESHEETS_V5.items()}


@router.get("/v5/blood-potency")
async def get_v5_blood_potency():
    """Get V5 blood potency table"""
    return {str(level): bp.model_dump() for level, bp in BLOOD_POTENCY_TABLE.items()}


@router.get("/v5/backgrounds")
async def get_v5_backgrounds():
    """Get all V5 backgrounds"""
    return {key: bg.model_dump() for key, bg in BACKGROUNDS_V5.items()}


@router.get("/v5/merits")
async def get_v5_merits():
    """Get all V5 merits"""
    return {key: merit.model_dump() for key, merit in MERITS_V5.items()}


@router.get("/v5/flaws")
async def get_v5_flaws():
    """Get all V5 flaws"""
    return {key: flaw.model_dump() for key, flaw in FLAWS_V5.items()}


@router.get("/v5/coterie-types")
async def get_v5_coterie_types():
    """Get all V5 coterie types"""
    return {key: ct.model_dump() for key, ct in COTERIE_TYPES_V5.items()}


@router.get("/v5/rituals")
async def get_v5_rituals():
    """Get all V5 Blood Sorcery rituals"""
    return {key: ritual.model_dump() for key, ritual in BLOOD_SORCERY_RITUALS_V5.items()}


# === V20 Game Data ===

@router.get("/v20/clans")
async def get_v20_clans():
    """Get all V20 clans"""
    return {key: clan.model_dump() for key, clan in CLANS_V20.items()}


@router.get("/v20/clans/{clan_id}")
async def get_v20_clan(clan_id: str):
    """Get a specific V20 clan"""
    clan = CLANS_V20.get(clan_id)
    if not clan:
        return {"error": "Clan not found"}
    return clan.model_dump()


@router.get("/v20/disciplines")
async def get_v20_disciplines():
    """Get all V20 disciplines"""
    return {key: disc.model_dump() for key, disc in DISCIPLINES_V20.items()}


@router.get("/v20/backgrounds")
async def get_v20_backgrounds():
    """Get all V20 backgrounds"""
    return BACKGROUNDS_V20
