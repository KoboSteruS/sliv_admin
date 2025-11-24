"""
Модель заявки/товара (products)
"""
from sqlalchemy import Column, BigInteger, Text, ForeignKey, Numeric, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func

from app.database import Base


class Product(Base):
    """
    Модель заявки/товара.
    Таблица: bo.products
    """
    __tablename__ = "products"
    __table_args__ = {"schema": "bo"}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, nullable=False)
    supplier_user_id = Column(
        BigInteger,
        ForeignKey("bo.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID пользователя (из таблицы bo.users), создавшего заявку",
    )
    category_id = Column(
        BigInteger,
        ForeignKey("bo.categories.id", ondelete="SET NULL"),
        nullable=False,
        index=True,
        comment="ID категории",
    )
    source_url = Column(Text, nullable=False, comment="URL источника товара")
    price_rub = Column(Numeric, nullable=False, comment="Цена в рублях")
    country_of_origin = Column(Text, nullable=True, comment="Страна происхождения")
    composition = Column(Text, nullable=True, comment="Состав")
    size_range = Column(Text, nullable=True, comment="Размерный ряд")
    color = Column(Text, nullable=True, comment="Цвет")
    description = Column(Text, nullable=True, comment="Описание товара")
    attributes = Column(JSONB, nullable=True, comment="Дополнительные атрибуты (JSON)")
    status_id = Column(
        BigInteger,
        ForeignKey("bo.statuses.id", ondelete="SET NULL"),
        nullable=False,
        index=True,
        comment="ID статуса",
    )
    approved_by = Column(BigInteger, nullable=True, comment="ID пользователя, который утвердил")
    approved_at = Column(DateTime(timezone=False), nullable=True, comment="Дата утверждения")
    is_active = Column(Boolean, nullable=False, server_default="true", comment="Активна ли заявка")
    created_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), comment="Дата создания")
    updated_at = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now(), comment="Дата обновления")
    
    # Связи
    supplier_account = relationship(
        "UserAccount",
        primaryjoin="UserAccount.id == foreign(Product.supplier_user_id)",
        viewonly=True,
        uselist=False,
    )
    status = relationship("Status", back_populates="products")
    category = relationship("Category", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, price={self.price_rub}, supplier_user_id={self.supplier_user_id})>"

