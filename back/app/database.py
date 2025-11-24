"""
Подключение к базе данных PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

from app.config import settings

# Создаём движок SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=5,  # Уменьшил размер пула
    max_overflow=10,  # Уменьшил overflow
    pool_timeout=30,  # Таймаут получения соединения из пула
    pool_recycle=3600,  # Переиспользование соединений каждый час
    connect_args={
        "connect_timeout": 30,  # Таймаут подключения к БД (увеличено для медленных соединений)
        "options": "-c statement_timeout=60000",  # Таймаут выполнения запроса (60 сек)
    },
    echo=False,  # Логирование SQL запросов (поставь True для отладки)
)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """
    Dependency для получения сессии БД.
    Используется в FastAPI через Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Ошибка работы с БД: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Инициализация БД (создание таблиц, если их нет)"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        raise

