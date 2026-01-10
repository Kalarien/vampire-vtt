from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Optional
import httpx
import uuid

from ..config import settings
from ..database import get_db
from ..models.user import User

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


@router.get("/discord")
async def discord_login():
    """Redirect to Discord OAuth"""
    if not settings.discord_client_id:
        raise HTTPException(status_code=500, detail="Discord OAuth not configured")

    discord_auth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={settings.discord_client_id}"
        f"&redirect_uri={settings.discord_redirect_uri}"
        f"&response_type=code"
        f"&scope=identify%20email"
    )
    return RedirectResponse(url=discord_auth_url)


@router.get("/discord/callback")
async def discord_callback(code: str):
    """Handle Discord OAuth callback"""
    if not settings.discord_client_id or not settings.discord_client_secret:
        raise HTTPException(status_code=500, detail="Discord OAuth not configured")

    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": settings.discord_client_id,
                "client_secret": settings.discord_client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.discord_redirect_uri,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get Discord token")

        token_data = token_response.json()
        access_token = token_data["access_token"]

        # Get user info
        user_response = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get Discord user")

        discord_user = user_response.json()

    # TODO: Create or update user in database

    # Create JWT token
    jwt_token = create_access_token(
        data={"sub": discord_user["id"], "discord_username": discord_user["username"]}
    )

    # Redirect to frontend with token
    frontend_url = settings.cors_origins[0] if settings.cors_origins else "http://localhost:5173"
    return RedirectResponse(url=f"{frontend_url}?token={jwt_token}")


@router.get("/me")
async def get_current_user_info():
    """Get current user info"""
    # TODO: Implement with proper auth
    return {"message": "Not implemented"}


# ============== EMAIL/PASSWORD LOGIN ==============

@router.post("/register")
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new user with email and password"""
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    # Check if username already exists
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Nome de usuario ja existe")

    # Create user
    user = User(
        id=str(uuid.uuid4()),
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password),
        discord_id=None
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Create JWT token
    jwt_token = create_access_token(
        data={
            "sub": user.id,
            "username": user.username
        }
    )

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar
        }
    }


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with email and password"""
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    if not user.password_hash:
        raise HTTPException(status_code=401, detail="Esta conta usa login via Discord")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    # Create JWT token
    jwt_token = create_access_token(
        data={
            "sub": user.id,
            "username": user.username
        }
    )

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar
        }
    }


# ============== DEV MODE LOGIN ==============
@router.get("/dev-login")
async def dev_login(username: str = "DevUser", db: AsyncSession = Depends(get_db)):
    """
    Development login - creates a test user without Discord OAuth.
    Only available in development mode.
    """
    if settings.ENVIRONMENT != "development":
        raise HTTPException(status_code=403, detail="Dev login only available in development")

    # Check if dev user exists
    dev_discord_id = f"dev_{username.lower()}"
    result = await db.execute(
        select(User).where(User.discord_id == dev_discord_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        # Create dev user
        user = User(
            id=str(uuid.uuid4()),
            discord_id=dev_discord_id,
            username=username,
            email=f"{username.lower()}@dev.local",
            avatar=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Create JWT token
    jwt_token = create_access_token(
        data={
            "sub": user.id,
            "discord_id": user.discord_id,
            "username": user.username
        }
    )

    # Return token and user info
    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar
        }
    }


# ============== PASSWORD RECOVERY ==============

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# Store reset tokens temporarily (in production, use Redis or similar)
password_reset_tokens: dict[str, tuple[str, datetime]] = {}


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Request a password reset"""
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    if not user:
        return {"message": "Se o email existir, um link de recuperacao sera enviado"}

    # Generate reset token
    reset_token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    password_reset_tokens[reset_token] = (user.id, expires_at)

    # In production: send email with reset link
    # For dev: log the token
    reset_url = f"http://localhost:5173/reset-password?token={reset_token}"
    print(f"[DEV] Password reset link for {data.email}: {reset_url}")

    return {"message": "Se o email existir, um link de recuperacao sera enviado"}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Reset password using token"""
    # Check if token exists and is valid
    if data.token not in password_reset_tokens:
        raise HTTPException(status_code=400, detail="Token invalido ou expirado")

    user_id, expires_at = password_reset_tokens[data.token]

    if datetime.utcnow() > expires_at:
        del password_reset_tokens[data.token]
        raise HTTPException(status_code=400, detail="Token expirado")

    # Find user
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    # Update password
    user.password_hash = get_password_hash(data.new_password)
    await db.commit()

    # Delete used token
    del password_reset_tokens[data.token]

    return {"message": "Senha alterada com sucesso"}


@router.get("/dev-login-redirect")
async def dev_login_redirect(username: str = "DevUser", db: AsyncSession = Depends(get_db)):
    """
    Development login with redirect - same as dev-login but redirects to frontend.
    """
    if settings.ENVIRONMENT != "development":
        raise HTTPException(status_code=403, detail="Dev login only available in development")

    # Check if dev user exists
    dev_discord_id = f"dev_{username.lower()}"
    result = await db.execute(
        select(User).where(User.discord_id == dev_discord_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        # Create dev user
        user = User(
            id=str(uuid.uuid4()),
            discord_id=dev_discord_id,
            username=username,
            email=f"{username.lower()}@dev.local",
            avatar=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Create JWT token
    jwt_token = create_access_token(
        data={
            "sub": user.id,
            "discord_id": user.discord_id,
            "username": user.username
        }
    )

    # Redirect to frontend with token
    return RedirectResponse(url=f"{settings.frontend_url}/auth/callback?token={jwt_token}")
