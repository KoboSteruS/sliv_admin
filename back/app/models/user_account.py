"""
Модель пользователя (users) — минимально необходимые поля
для установления связей (FK) и выборок по tg_user_id.
"""
from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func

from app.database import Base


class UserAccount(Base):
    """
    Модель таблицы bo.users (минимально необходимые поля).
    """

    __tablename__ = "users"
    __table_args__ = {"schema": "bo"}

    id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    tg_user_id = Column(BigInteger, nullable=True, comment="ID пользователя в Telegram")
    phone = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    username = Column(Text, nullable=True)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    is_client = Column(Boolean, nullable=False, server_default="false")
    role = Column(Text, nullable=False, server_default="client")
    deeplink_ref = Column(Text, nullable=True)
    registered_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())
    paid_until = Column(DateTime(timezone=False), nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now())

    # Связь с поставщиком через tg_user_id
    supplier_profile = relationship(
        "Supplier",
        primaryjoin="foreign(Supplier.tg_user_id) == UserAccount.tg_user_id",
        viewonly=True,
        uselist=False,
    )

    def __repr__(self):
        return f"<UserAccount(id={self.id}, tg_user_id={self.tg_user_id})>"


