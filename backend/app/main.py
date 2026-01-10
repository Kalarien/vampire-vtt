from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db
from .api import auth, users, chronicles, characters, dice, scenes, game_data, websocket, xp, sessions, chat, initiative


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title=settings.app_name,
    description="Virtual Tabletop para Vampire: The Masquerade (V5 e V20)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(chronicles.router, prefix="/api/chronicles", tags=["Chronicles"])
app.include_router(characters.router, prefix="/api/characters", tags=["Characters"])
app.include_router(dice.router, prefix="/api/dice", tags=["Dice"])
app.include_router(scenes.router, prefix="/api/scenes", tags=["Scenes"])
app.include_router(game_data.router, prefix="/api/game-data", tags=["Game Data"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
app.include_router(xp.router, prefix="/api/xp", tags=["XP"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(initiative.router, prefix="/api/initiative", tags=["Initiative"])


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "Virtual Tabletop para Vampire: The Masquerade",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
