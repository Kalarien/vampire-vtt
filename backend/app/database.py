from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings


# Get database URL and convert for async
database_url = settings.database_url

# Convert postgres:// or postgresql:// to postgresql+asyncpg://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgresql://") and "+asyncpg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Determine if using SQLite
is_sqlite = database_url.startswith("sqlite")

# Create async engine with appropriate settings
engine_kwargs = {
    "echo": settings.debug,
    "future": True,
}

# SQLite needs check_same_thread=False for async
if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(
    database_url,
    **engine_kwargs
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_async_session():
    """Get async session for non-dependency contexts (like websocket)"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
