"""
Модель поставщика (suppliers)
"""
from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func

from app.database import Base


class Supplier(Base):
    """
    Модель поставщика.
    Таблица: bo.suppliers
    """
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "bo"}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, nullable=False)
    tg_user_id = Column(BigInteger, nullable=True, comment="Telegram user ID")
    phone = Column(Text, nullable=True, comment="Телефон")
    email = Column(Text, nullable=True, comment="Email")
    username = Column(Text, nullable=True, comment="Username")
    first_name = Column(Text, nullable=True, comment="Имя")
    last_name = Column(Text, nullable=True, comment="Фамилия")
    custom_name = Column(Text, nullable=True, comment="Кастомное имя")
    is_supplier = Column(Boolean, nullable=False, comment="Является поставщиком")
    role = Column(Text, nullable=False, comment="Роль пользователя")
    deeplink_ref = Column(Text, nullable=True, comment="Реферальная ссылка")
    registered_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), comment="Дата регистрации")
    token = Column(Text, nullable=True, unique=True, index=True, comment="Токен для входа")
    
    def __repr__(self):
        name = self.custom_name or self.first_name or self.username or f"ID:{self.id}"
        return f"<Supplier(id={self.id}, name={name}, role={self.role})>"

