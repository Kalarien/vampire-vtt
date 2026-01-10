from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models.scene import Scene
from ..models.chronicle import Chronicle, ChronicleMember
from ..models.user import User
from .deps import get_current_user

router = APIRouter()


class SceneCreate(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None


class SceneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class SceneResponse(BaseModel):
    id: str
    chronicle_id: str
    name: str
    description: Optional[str]
    location: Optional[str]
    image_url: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


async def get_chronicle_with_access(
    db: AsyncSession,
    chronicle_id: str,
    user_id: str,
    require_storyteller: bool = False
) -> Chronicle:
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
    if not is_member and not is_storyteller:
        raise HTTPException(status_code=403, detail="Acesso negado")
    if require_storyteller and not is_storyteller:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode fazer isso")
    return chronicle


async def get_scene_with_access(
    db: AsyncSession,
    scene_id: str,
    user_id: str,
    require_storyteller: bool = False
) -> tuple:
    result = await db.execute(
        select(Scene)
        .where(Scene.id == scene_id)
        .options(selectinload(Scene.chronicle).selectinload(Chronicle.members))
    )
    scene = result.scalar_one_or_none()
    if not scene:
        raise HTTPException(status_code=404, detail="Cena nao encontrada")
    chronicle = scene.chronicle
    is_storyteller = chronicle.storyteller_id == user_id
    is_member = any(m.user_id == user_id for m in chronicle.members)
    if not is_member and not is_storyteller:
        raise HTTPException(status_code=403, detail="Acesso negado")
    if require_storyteller and not is_storyteller:
        raise HTTPException(status_code=403, detail="Apenas o Narrador pode fazer isso")
    return scene, chronicle


@router.get("/{chronicle_id}", response_model=List[SceneResponse])
async def list_scenes(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_chronicle_with_access(db, chronicle_id, current_user.id)
    result = await db.execute(
        select(Scene)
        .where(Scene.chronicle_id == chronicle_id)
        .order_by(Scene.created_at.desc())
    )
    scenes = result.scalars().all()
    return [
        {"id": s.id, "chronicle_id": s.chronicle_id, "name": s.name,
         "description": s.description, "location": s.location,
         "image_url": s.image_url, "is_active": s.is_active}
        for s in scenes
    ]


@router.get("/{chronicle_id}/active")
async def get_active_scene(
    chronicle_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_chronicle_with_access(db, chronicle_id, current_user.id)
    result = await db.execute(
        select(Scene)
        .where(Scene.chronicle_id == chronicle_id)
        .where(Scene.is_active == True)
    )
    scene = result.scalar_one_or_none()
    if not scene:
        return None
    return {
        "id": scene.id, "chronicle_id": scene.chronicle_id, "name": scene.name,
        "description": scene.description, "location": scene.location,
        "image_url": scene.image_url, "is_active": scene.is_active
    }


@router.post("/{chronicle_id}", status_code=status.HTTP_201_CREATED)
async def create_scene(
    chronicle_id: str,
    scene_data: SceneCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_chronicle_with_access(db, chronicle_id, current_user.id, require_storyteller=True)
    scene = Scene(
        id=str(uuid.uuid4()),
        chronicle_id=chronicle_id,
        name=scene_data.name,
        description=scene_data.description,
        location=scene_data.location,
        image_url=scene_data.image_url,
        is_active=False,
    )
    db.add(scene)
    await db.commit()
    await db.refresh(scene)
    return {
        "id": scene.id, "chronicle_id": scene.chronicle_id, "name": scene.name,
        "description": scene.description, "location": scene.location,
        "image_url": scene.image_url, "is_active": scene.is_active
    }


@router.post("/{scene_id}/activate")
async def activate_scene(
    scene_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scene, chronicle = await get_scene_with_access(db, scene_id, current_user.id, require_storyteller=True)
    result = await db.execute(select(Scene).where(Scene.chronicle_id == chronicle.id))
    all_scenes = result.scalars().all()
    for s in all_scenes:
        s.is_active = (s.id == scene_id)
    await db.commit()
    await db.refresh(scene)
    return {
        "id": scene.id, "chronicle_id": scene.chronicle_id, "name": scene.name,
        "description": scene.description, "location": scene.location,
        "image_url": scene.image_url, "is_active": scene.is_active
    }


@router.post("/{scene_id}/deactivate")
async def deactivate_scene(
    scene_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scene, _ = await get_scene_with_access(db, scene_id, current_user.id, require_storyteller=True)
    scene.is_active = False
    await db.commit()
    await db.refresh(scene)
    return {
        "id": scene.id, "chronicle_id": scene.chronicle_id, "name": scene.name,
        "description": scene.description, "location": scene.location,
        "image_url": scene.image_url, "is_active": scene.is_active
    }


@router.patch("/{scene_id}")
async def update_scene(
    scene_id: str,
    scene_data: SceneUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scene, chronicle = await get_scene_with_access(db, scene_id, current_user.id, require_storyteller=True)
    if scene_data.name is not None:
        scene.name = scene_data.name
    if scene_data.description is not None:
        scene.description = scene_data.description
    if scene_data.location is not None:
        scene.location = scene_data.location
    if scene_data.image_url is not None:
        scene.image_url = scene_data.image_url
    if scene_data.is_active is not None:
        if scene_data.is_active:
            result = await db.execute(select(Scene).where(Scene.chronicle_id == chronicle.id))
            all_scenes = result.scalars().all()
            for s in all_scenes:
                s.is_active = (s.id == scene_id)
        else:
            scene.is_active = False
    await db.commit()
    await db.refresh(scene)
    return {
        "id": scene.id, "chronicle_id": scene.chronicle_id, "name": scene.name,
        "description": scene.description, "location": scene.location,
        "image_url": scene.image_url, "is_active": scene.is_active
    }


@router.delete("/{scene_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scene(
    scene_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scene, _ = await get_scene_with_access(db, scene_id, current_user.id, require_storyteller=True)
    await db.delete(scene)
    await db.commit()
