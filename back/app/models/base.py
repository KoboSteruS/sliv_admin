"""
Базовая модель с общими полями
"""
from sqlalchemy import Column, BigInteger, DateTime, func
from datetime import datetime

from app.database import Base


class BaseModel(Base):
    """
    Базовый класс для всех моделей.
    Содержит общие поля: id (bigint), created_at, updated_at
    """
    __abstract__ = True
    
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False,
    )
    
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        comment="Дата создания записи",
    )
    
    updated_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Дата последнего обновления записи",
    )

