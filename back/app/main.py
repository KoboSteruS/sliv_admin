"""
Главный файл приложения FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.api.v1 import api_router

# Настраиваем логирование
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Создаём приложение
app = FastAPI(
    title="Sliv Admin API",
    description="Backend API для админ-панели Sliv",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["health"])
async def root():
    """Проверка работоспособности API"""
    return {
        "message": "Sliv Admin API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint - не использует БД"""
    return {"status": "ok", "message": "API работает"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8100,
        reload=True,
    )

