from datetime import datetime, timedelta
from typing import Optional
import httpx
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.user import User


class AuthService:
    """Service for handling authentication"""

    DISCORD_API_URL = "https://discord.com/api/v10"
    ALGORITHM = "HS256"

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=AuthService.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[AuthService.ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def get_discord_oauth_url() -> str:
        """Generate Discord OAuth URL"""
        params = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "redirect_uri": settings.DISCORD_REDIRECT_URI,
            "response_type": "code",
            "scope": "identify email",
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"https://discord.com/oauth2/authorize?{query}"

    @staticmethod
    async def exchange_code(code: str) -> Optional[dict]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "client_secret": settings.DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.DISCORD_REDIRECT_URI,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AuthService.DISCORD_API_URL}/oauth2/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code != 200:
                return None

            return response.json()

    @staticmethod
    async def get_discord_user(access_token: str) -> Optional[dict]:
        """Get Discord user info from access token"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AuthService.DISCORD_API_URL}/users/@me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code != 200:
                return None

            return response.json()

    @staticmethod
    async def get_or_create_user(
        db: AsyncSession,
        discord_user: dict
    ) -> User:
        """Get existing user or create new one from Discord data"""
        discord_id = discord_user["id"]

        # Try to find existing user
        result = await db.execute(
            select(User).where(User.discord_id == discord_id)
        )
        user = result.scalar_one_or_none()

        if user:
            # Update user info
            user.username = discord_user["username"]
            user.avatar = discord_user.get("avatar")
            user.email = discord_user.get("email")
            await db.commit()
            await db.refresh(user)
            return user

        # Create new user
        user = User(
            discord_id=discord_id,
            username=discord_user["username"],
            avatar=discord_user.get("avatar"),
            email=discord_user.get("email"),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


auth_service = AuthService()
