from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.database.database import create_tables
from app.routers import advertisements

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Ожидание запуска базы данных...")
    await asyncio.sleep(10)
    
    success = await create_tables()
    if success:
        print("Приложение готово к работе")
    else:
        print("Приложение запущено, но таблицы не созданы")
    
    yield
    
    print("Приложение завершает работу...")

app = FastAPI(
    title="Advertisement API",
    description="API для объявлений купли/продажи",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(advertisements.router)

@app.get("/")
async def root():
    return {"message": "Advertisement API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API работает"}

@app.get("/db-status")
async def db_status():
    try:
        from app.database.database import create_tables
        success = await create_tables()
        return {"database_status": "connected" if success else "disconnected"}
    except Exception as e:
        return {"database_status": "error", "details": str(e)}