"""
Модель статуса (statuses)
"""
from sqlalchemy import Column, BigInteger, String, Text, Integer, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Status(Base):
    """
    Модель статуса.
    Таблица: bo.statuses
    """
    __tablename__ = "statuses"
    __table_args__ = {"schema": "bo"}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, nullable=True)
    entity_type = Column(Text, nullable=True, comment="Тип сущности (product, etc)")
    code = Column(Text, nullable=True, comment="Код статуса")
    name = Column(Text, nullable=True, comment="Название статуса")
    color = Column(Text, nullable=True, comment="Цвет для отображения")
    order_index = Column(Integer, nullable=True, comment="Порядок сортировки")
    is_final = Column(Boolean, nullable=True, comment="Финальный ли статус")
    can_transition_to = Column(JSONB, nullable=True, comment="В какие статусы можно перейти")
    created_at = Column(DateTime(timezone=False), nullable=True, server_default=func.now(), comment="Дата создания")
    
    # Связи
    products = relationship("Product", back_populates="status")
    
    def __repr__(self):
        return f"<Status(id={self.id}, name={self.name}, code={self.code})>"

