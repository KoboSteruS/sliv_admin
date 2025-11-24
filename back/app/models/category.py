"""
Модель категории (categories)
"""
from sqlalchemy import Column, BigInteger, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    """
    Модель категории.
    Таблица: bo.categories
    """
    __tablename__ = "categories"
    __table_args__ = {"schema": "bo"}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, nullable=True)
    code = Column(Text, nullable=True, comment="Код категории")
    name = Column(Text, nullable=True, comment="Название категории")
    required_fields = Column(JSONB, nullable=True, comment="Обязательные поля")
    attributes_schema = Column(JSONB, nullable=True, comment="Схема атрибутов")
    created_at = Column(DateTime(timezone=False), nullable=True, server_default=func.now(), comment="Дата создания")
    
    # Связи
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, code={self.code})>"

