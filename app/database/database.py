import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# ИСПРАВЛЕНИЕ: Получаем переменные окружения отдельно
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "advertisements")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# ИСПРАВЛЕНИЕ: Собираем URL вручную для отладки
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(f"Подключаемся к БД: postgresql://{POSTGRES_USER}:****@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

# ИСПРАВЛЕНИЕ: Увеличиваем таймауты и добавляем параметры для лучшей устойчивости
engine = create_async_engine(
    DATABASE_URL, 
    echo=True, 
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "server_settings": {
            "jit": "off"
        }
    }
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ИСПРАВЛЕНИЕ: Простая функция для создания таблиц с одной попыткой
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Таблицы успешно созданы")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        return False