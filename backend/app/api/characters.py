from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified
from typing import Optional, Dict, Any
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models.character import Character
from ..models.chronicle import Chronicle, ChronicleMember
from ..models.user import User
from ..models.sheet_change_log import SheetChangeLog
from .deps import get_current_user

router = APIRouter()


class CharacterCreate(BaseModel):
    name: str
    concept: Optional[str] = None
    clan: Optional[str] = None
    generation: Optional[int] = None
    predator_type: Optional[str] = None
    nature: Optional[str] = None
    demeanor: Optional[str] = None
    game_version: str = "v5"
    chronicle_id: Optional[str] = None
    sheet: Dict[str, Any] = {}


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    concept: Optional[str] = None
    clan: Optional[str] = None
    generation: Optional[int] = None
    predator_type: Optional[str] = None
    nature: Optional[str] = None
    demeanor: Optional[str] = None
    portrait_url: Optional[str] = None


class SheetUpdate(BaseModel):
    sheet: Dict[str, Any]
    reason: Optional[str] = None  # Motivo da alteracao (usado pelo narrador)


class CharacterApproval(BaseModel):
    message: Optional[str] = None


class SubmitChanges(BaseModel):
    sheet: Dict[str, Any]
    justification: Optional[str] = None


def character_to_dict(character: Character) -> dict:
    return {
        "id": character.id,
        "name": character.name,
        "concept": character.concept,
        "clan": character.clan,
        "generation": character.generation,
        "predator_type": character.predator_type,
        "nature": character.nature,
        "demeanor": character.demeanor,
        "owner_id": character.owner_id,
        "chronicle_id": character.chronicle_id,
        "game_version": character.game_version,
        "sheet": character.sheet or {},
        "is_npc": character.is_npc,
        "portrait_url": character.portrait_url,
        "approval_status": character.approval_status or "draft",
        "pending_sheet": character.pending_sheet,
        "storyteller_notes": character.storyteller_notes,
        "created_at": character.created_at.isoformat() if character.created_at else None,
        "updated_at": character.updated_at.isoformat() if character.updated_at else None,
    }


@router.get("/")
async def list_characters(
    chronicle_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Character).where(Character.owner_id == current_user.id)
    if chronicle_id:
        query = query.where(Character.chronicle_id == chronicle_id)
    result = await db.execute(query.order_by(Character.name))
    characters = result.scalars().all()
    return [character_to_dict(c) for c in characters]


@router.get("/chronicle/{chronicle_id}/pending")
async def list_pending_approvals(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all characters pending approval in a chronicle (storyteller only)"""
    chronicle_result = await db.execute(
        select(Chronicle).where(Chronicle.id == chronicle_id)
    )
    chronicle = chronicle_result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Cronica nao encontrada")

    if chronicle.storyteller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode ver personagens pendentes")

    result = await db.execute(
        select(Character)
        .where(Character.chronicle_id == chronicle_id)
        .where(Character.approval_status == "pending")
        .options(selectinload(Character.owner))
    )
    characters = result.scalars().all()

    return [
        {
            **character_to_dict(c),
            "owner_name": c.owner.username if c.owner else "Desconhecido"
        }
        for c in characters
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_character(
    character_data: CharacterCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if character_data.chronicle_id:
        member_result = await db.execute(
            select(ChronicleMember)
            .where(ChronicleMember.chronicle_id == character_data.chronicle_id)
            .where(ChronicleMember.user_id == current_user.id)
        )
        member = member_result.scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=403, detail="You must be a member of the chronicle")

    initial_sheet = dict(character_data.sheet) if character_data.sheet else {}

    if character_data.game_version == "v5":
        # V5 - Vampire: The Masquerade 5th Edition
        if "atributos" not in initial_sheet:
            initial_sheet["atributos"] = {
                "fisicos": {"forca": 1, "destreza": 1, "vigor": 1},
                "sociais": {"carisma": 1, "manipulacao": 1, "compostura": 1},
                "mentais": {"inteligencia": 1, "raciocinio": 1, "determinacao": 1},
            }
        if "habilidades" not in initial_sheet:
            initial_sheet["habilidades"] = {
                "atletismo": 0, "briga": 0, "conducao": 0, "armasDeFogo": 0,
                "armasBrancas": 0, "furtividade": 0, "furto": 0, "oficio": 0,
                "sobrevivencia": 0, "empatiaComAnimais": 0,
                "etiqueta": 0, "intimidacao": 0, "lideranca": 0, "manha": 0,
                "performance": 0, "persuasao": 0, "perspicacia": 0, "labia": 0,
                "academicos": 0, "ciencia": 0, "consciencia": 0, "financas": 0,
                "investigacao": 0, "medicina": 0, "ocultismo": 0, "politica": 0,
                "tecnologia": 0,
            }
        if "disciplinas" not in initial_sheet:
            initial_sheet["disciplinas"] = {}
        if "vitalidade" not in initial_sheet:
            initial_sheet["vitalidade"] = {"max": 3, "superficial": 0, "agravado": 0}
        if "forcaDeVontade" not in initial_sheet:
            initial_sheet["forcaDeVontade"] = {"max": 3, "superficial": 0, "agravado": 0}
        if "fome" not in initial_sheet:
            initial_sheet["fome"] = 1
        if "humanidade" not in initial_sheet:
            initial_sheet["humanidade"] = 7
        if "potenciaDeSangue" not in initial_sheet:
            initial_sheet["potenciaDeSangue"] = 1
        if "experiencia" not in initial_sheet:
            initial_sheet["experiencia"] = {"total": 0, "gasta": 0}
        if "ressonancia" not in initial_sheet:
            initial_sheet["ressonancia"] = ""
        if "desejo" not in initial_sheet:
            initial_sheet["desejo"] = ""
        if "ambicao" not in initial_sheet:
            initial_sheet["ambicao"] = ""
        if "convicoes" not in initial_sheet:
            initial_sheet["convicoes"] = []
        if "toquesDasMarcas" not in initial_sheet:
            initial_sheet["toquesDasMarcas"] = []
        if "defeitos" not in initial_sheet:
            initial_sheet["defeitos"] = []
        if "vantagens" not in initial_sheet:
            initial_sheet["vantagens"] = []
    else:
        # V20 - Vampire: The Masquerade 20th Anniversary
        if "atributos" not in initial_sheet:
            initial_sheet["atributos"] = {
                "fisicos": {"forca": 1, "destreza": 1, "vigor": 1},
                "sociais": {"carisma": 1, "manipulacao": 1, "aparencia": 1},
                "mentais": {"percepcao": 1, "inteligencia": 1, "raciocinio": 1},
            }
        if "habilidades" not in initial_sheet:
            initial_sheet["habilidades"] = {
                "talentos": {
                    "prontidao": 0, "atletismo": 0, "briga": 0, "consciencia": 0,
                    "empatia": 0, "expressao": 0, "intimidacao": 0, "lideranca": 0,
                    "manha": 0, "labia": 0,
                },
                "pericias": {
                    "empatiaComAnimais": 0, "oficios": 0, "conducao": 0, "etiqueta": 0,
                    "armasDeFogo": 0, "armasBrancas": 0, "performance": 0, "seguranca": 0,
                    "furtividade": 0, "sobrevivencia": 0,
                },
                "conhecimentos": {
                    "academicos": 0, "computador": 0, "financas": 0, "investigacao": 0,
                    "direito": 0, "linguistica": 0, "medicina": 0, "ocultismo": 0,
                    "politica": 0, "ciencia": 0,
                },
            }
        if "disciplinas" not in initial_sheet:
            initial_sheet["disciplinas"] = {}
        if "antecedentes" not in initial_sheet:
            initial_sheet["antecedentes"] = {}
        if "virtudes" not in initial_sheet:
            initial_sheet["virtudes"] = {"consciencia": 1, "autocontrole": 1, "coragem": 1}
        if "vitalidade" not in initial_sheet:
            initial_sheet["vitalidade"] = {"max": 7, "contusao": 0, "letal": 0, "agravado": 0}
        if "forcaDeVontade" not in initial_sheet:
            initial_sheet["forcaDeVontade"] = {"permanente": 3, "temporaria": 3}
        if "pontoDeSangue" not in initial_sheet:
            initial_sheet["pontoDeSangue"] = {"max": 10, "atual": 10}
        if "humanidade" not in initial_sheet:
            initial_sheet["humanidade"] = 7
        if "experiencia" not in initial_sheet:
            initial_sheet["experiencia"] = {"total": 0, "gasta": 0}
        if "qualidades" not in initial_sheet:
            initial_sheet["qualidades"] = []
        if "defeitos" not in initial_sheet:
            initial_sheet["defeitos"] = []

    character = Character(
        id=str(uuid.uuid4()),
        name=character_data.name,
        concept=character_data.concept,
        clan=character_data.clan,
        generation=character_data.generation,
        predator_type=character_data.predator_type,
        nature=character_data.nature,
        demeanor=character_data.demeanor,
        owner_id=current_user.id,
        chronicle_id=character_data.chronicle_id,
        game_version=character_data.game_version,
        sheet=initial_sheet,
        is_npc=False,
    )

    db.add(character)
    await db.commit()
    await db.refresh(character)
    return character_to_dict(character)


@router.get("/{character_id}")
async def get_character(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Character)
        .where(Character.id == character_id)
        .options(selectinload(Character.chronicle))
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Owner can always see their own character
    if character.owner_id == current_user.id:
        return character_to_dict(character)

    # If character is in a chronicle, check if user is the storyteller
    if character.chronicle_id and character.chronicle:
        if character.chronicle.storyteller_id == current_user.id:
            return character_to_dict(character)

    # Other players cannot see character sheets that aren't theirs
    raise HTTPException(status_code=403, detail="Voce so pode ver sua propria ficha")


@router.patch("/{character_id}")
async def update_character(
    character_id: str,
    character_data: CharacterUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can update character")

    update_data = character_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(character, field, value)

    await db.commit()
    await db.refresh(character)
    return character_to_dict(character)


@router.patch("/{character_id}/sheet")
async def update_character_sheet(
    character_id: str,
    sheet_update: SheetUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    is_owner = character.owner_id == current_user.id
    is_storyteller = False
    is_in_chronicle = character.chronicle_id is not None

    if character.chronicle_id:
        chronicle_result = await db.execute(
            select(Chronicle).where(Chronicle.id == character.chronicle_id)
        )
        chronicle = chronicle_result.scalar_one_or_none()
        if chronicle and chronicle.storyteller_id == current_user.id:
            is_storyteller = True

    if not is_owner and not is_storyteller:
        raise HTTPException(status_code=403, detail="Only owner or storyteller can update sheet")

    # REGRA: Se o personagem esta em uma cronica e o jogador (dono) tenta editar,
    # a mudanca vai para pending_sheet e precisa de aprovacao do narrador
    if is_in_chronicle and is_owner and not is_storyteller:
        # Verificar se ja tem mudancas pendentes
        if character.pending_sheet:
            raise HTTPException(
                status_code=400,
                detail="Voce ja tem alteracoes pendentes de aprovacao. Aguarde o Narrador revisar."
            )

        # Salvar mudancas como pendentes
        character.pending_sheet = sheet_update.sheet
        character.approval_status = "pending"
        character.storyteller_notes = sheet_update.reason or "Alteracoes propostas pelo jogador"

        await db.commit()
        await db.refresh(character)

        return {
            **character_to_dict(character),
            "pending_approval": True,
            "message": "Alteracoes enviadas para aprovacao do Narrador"
        }

    # Edicao direta (personagem sem cronica OU narrador editando)
    current_sheet = dict(character.sheet) if character.sheet else {}
    current_sheet.update(sheet_update.sheet)
    character.sheet = current_sheet
    flag_modified(character, 'sheet')  # Force SQLAlchemy to detect JSON change

    # Se o storyteller alterou a ficha de outro jogador, registrar a mudanca
    if is_storyteller and not is_owner:
        change_log = SheetChangeLog(
            id=str(uuid.uuid4()),
            character_id=character_id,
            storyteller_id=current_user.id,
            changes=sheet_update.sheet,
            reason=sheet_update.reason or "Alteracao feita pelo Narrador",
            seen=False,
        )
        db.add(change_log)

    await db.commit()
    await db.refresh(character)

    response = character_to_dict(character)
    if is_storyteller and not is_owner:
        response["storyteller_change"] = True
        response["change_reason"] = sheet_update.reason or "Alteracao feita pelo Narrador"

    return response


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can delete character")

    await db.delete(character)
    await db.commit()


@router.post("/{character_id}/assign/{chronicle_id}")
async def assign_to_chronicle(
    character_id: str,
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    char_result = await db.execute(select(Character).where(Character.id == character_id))
    character = char_result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can assign character")

    member_result = await db.execute(
        select(ChronicleMember)
        .where(ChronicleMember.chronicle_id == chronicle_id)
        .where(ChronicleMember.user_id == current_user.id)
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="You must be a member of the chronicle")

    chronicle_result = await db.execute(select(Chronicle).where(Chronicle.id == chronicle_id))
    chronicle = chronicle_result.scalar_one_or_none()

    if not chronicle:
        raise HTTPException(status_code=404, detail="Chronicle not found")

    if chronicle.game_version != character.game_version:
        raise HTTPException(
            status_code=400,
            detail=f"Character version ({character.game_version}) doesn't match chronicle ({chronicle.game_version})"
        )

    character.chronicle_id = chronicle_id
    character.approval_status = "pending"  # Needs storyteller approval
    character.storyteller_notes = None
    await db.commit()
    await db.refresh(character)
    return character_to_dict(character)


@router.post("/{character_id}/submit-for-approval")
async def submit_for_approval(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit character for storyteller approval"""
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o dono pode submeter o personagem")

    if not character.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem precisa estar em uma cronica")

    if character.approval_status == "pending":
        raise HTTPException(status_code=400, detail="Personagem ja esta aguardando aprovacao")

    character.approval_status = "pending"
    character.storyteller_notes = None
    await db.commit()
    await db.refresh(character)
    return {"message": "Personagem enviado para aprovacao", "character": character_to_dict(character)}


@router.post("/{character_id}/approve")
async def approve_character(
    character_id: str,
    data: CharacterApproval,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Approve a character (storyteller only)"""
    result = await db.execute(
        select(Character)
        .where(Character.id == character_id)
        .options(selectinload(Character.chronicle))
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if not character.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem nao esta em uma cronica")

    chronicle = character.chronicle
    if chronicle.storyteller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode aprovar personagens")

    if character.approval_status != "pending":
        raise HTTPException(status_code=400, detail="Personagem nao esta aguardando aprovacao")

    # If there are pending changes, apply them
    if character.pending_sheet:
        current_sheet = dict(character.sheet) if character.sheet else {}
        current_sheet.update(character.pending_sheet)
        character.sheet = current_sheet
        flag_modified(character, 'sheet')  # Force SQLAlchemy to detect JSON change
        character.pending_sheet = None

    character.approval_status = "approved"
    character.storyteller_notes = data.message
    await db.commit()
    await db.refresh(character)
    return {"message": "Personagem aprovado", "character": character_to_dict(character)}


@router.post("/{character_id}/reject")
async def reject_character(
    character_id: str,
    data: CharacterApproval,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reject a character (storyteller only)"""
    result = await db.execute(
        select(Character)
        .where(Character.id == character_id)
        .options(selectinload(Character.chronicle))
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if not character.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem nao esta em uma cronica")

    chronicle = character.chronicle
    if chronicle.storyteller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode rejeitar personagens")

    if character.approval_status != "pending":
        raise HTTPException(status_code=400, detail="Personagem nao esta aguardando aprovacao")

    character.approval_status = "rejected"
    character.pending_sheet = None  # Clear pending changes
    character.storyteller_notes = data.message
    await db.commit()
    await db.refresh(character)
    return {"message": "Personagem rejeitado", "character": character_to_dict(character)}


@router.post("/{character_id}/submit-changes")
async def submit_sheet_changes(
    character_id: str,
    data: SubmitChanges,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit sheet changes for approval (for approved characters)"""
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o dono pode modificar o personagem")

    if not character.chronicle_id:
        raise HTTPException(status_code=400, detail="Personagem precisa estar em uma cronica")

    if character.approval_status != "approved":
        raise HTTPException(status_code=400, detail="Personagem precisa estar aprovado primeiro")

    if character.pending_sheet:
        raise HTTPException(status_code=400, detail="Ja existem mudancas pendentes de aprovacao")

    character.pending_sheet = data.sheet
    character.approval_status = "pending"
    character.storyteller_notes = f"Mudancas propostas: {data.justification or 'Sem justificativa'}"
    await db.commit()
    await db.refresh(character)
    return {"message": "Mudancas enviadas para aprovacao", "character": character_to_dict(character)}


@router.post("/{character_id}/unassign")
async def unassign_from_chronicle(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Character)
        .where(Character.id == character_id)
        .options(selectinload(Character.chronicle))
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Check if user is owner or storyteller of the chronicle
    is_owner = character.owner_id == current_user.id
    is_storyteller = False
    if character.chronicle_id and character.chronicle:
        is_storyteller = character.chronicle.storyteller_id == current_user.id

    if not is_owner and not is_storyteller:
        raise HTTPException(status_code=403, detail="Only owner or storyteller can remove character")

    character.chronicle_id = None
    character.approval_status = "draft"  # Reset approval status
    character.pending_sheet = None
    character.storyteller_notes = None
    await db.commit()
    await db.refresh(character)
    return character_to_dict(character)


@router.get("/{character_id}/notifications")
async def get_character_notifications(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get unread change notifications for a character"""
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    # Only owner can see notifications
    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o dono pode ver notificacoes")

    result = await db.execute(
        select(SheetChangeLog)
        .where(SheetChangeLog.character_id == character_id)
        .where(SheetChangeLog.seen == False)
        .options(selectinload(SheetChangeLog.storyteller))
        .order_by(SheetChangeLog.created_at.desc())
    )
    notifications = result.scalars().all()

    return [
        {
            "id": n.id,
            "changes": n.changes,
            "reason": n.reason,
            "storyteller_name": n.storyteller.username if n.storyteller else "Narrador",
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in notifications
    ]


@router.post("/{character_id}/notifications/mark-seen")
async def mark_notifications_seen(
    character_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark all notifications for a character as seen"""
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Personagem nao encontrado")

    if character.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o dono pode marcar notificacoes")

    # Update all unseen notifications
    from sqlalchemy import update
    await db.execute(
        update(SheetChangeLog)
        .where(SheetChangeLog.character_id == character_id)
        .where(SheetChangeLog.seen == False)
        .values(seen=True)
    )
    await db.commit()

    return {"message": "Notificacoes marcadas como vistas"}
