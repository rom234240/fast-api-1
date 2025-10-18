from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.database import create_tables
from app.routers import advertisements

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

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