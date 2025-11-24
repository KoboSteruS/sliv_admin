"""
Схемы для работы с заявками (products)
"""
from typing import Optional, Any
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """Базовая схема продукта"""
    source_url: str = Field(..., description="URL источника товара")
    price_rub: Decimal = Field(..., description="Цена в рублях")
    category_id: int = Field(..., description="ID категории")
    status_id: int = Field(..., description="ID статуса")
    country_of_origin: Optional[str] = Field(None, description="Страна происхождения")
    composition: Optional[str] = Field(None, description="Состав")
    size_range: Optional[str] = Field(None, description="Размерный ряд")
    color: Optional[str] = Field(None, description="Цвет")
    description: Optional[str] = Field(None, description="Описание товара")
    attributes: Optional[dict[str, Any]] = Field(None, description="Дополнительные атрибуты")
    is_active: bool = Field(True, description="Активна ли заявка")


class ProductCreate(BaseModel):
    """Схема для создания продукта"""
    source_url: str = Field(..., description="URL источника товара")
    price_rub: Decimal = Field(..., description="Цена в рублях")
    category_id: int = Field(..., description="ID категории")
    status_id: Optional[int] = Field(None, description="ID статуса (если не указан, устанавливается 'новый')")
    supplier_user_id: Optional[int] = Field(None, description="ID поставщика (устанавливается автоматически из токена)")
    country_of_origin: Optional[str] = Field(None, description="Страна происхождения")
    composition: Optional[str] = Field(None, description="Состав")
    size_range: Optional[str] = Field(None, description="Размерный ряд")
    color: Optional[str] = Field(None, description="Цвет")
    description: Optional[str] = Field(None, description="Описание товара")
    attributes: Optional[dict[str, Any]] = Field(None, description="Дополнительные атрибуты")
    is_active: bool = Field(True, description="Активна ли заявка")


class ProductUpdate(BaseModel):
    """Схема для обновления продукта"""
    source_url: Optional[str] = Field(None, description="URL источника товара")
    price_rub: Optional[Decimal] = Field(None, description="Цена в рублях")
    category_id: Optional[int] = Field(None, description="ID категории")
    status_id: Optional[int] = Field(None, description="ID статуса")
    country_of_origin: Optional[str] = Field(None, description="Страна происхождения")
    composition: Optional[str] = Field(None, description="Состав")
    size_range: Optional[str] = Field(None, description="Размерный ряд")
    color: Optional[str] = Field(None, description="Цвет")
    description: Optional[str] = Field(None, description="Описание товара")
    attributes: Optional[dict[str, Any]] = Field(None, description="Дополнительные атрибуты")
    is_active: Optional[bool] = Field(None, description="Активна ли заявка")


class StatusInfo(BaseModel):
    """Информация о статусе"""
    id: int
    name: Optional[str] = None
    code: Optional[str] = None


class CategoryInfo(BaseModel):
    """Информация о категории"""
    id: int
    name: Optional[str] = None
    code: Optional[str] = None


class SupplierInfo(BaseModel):
    """Информация о поставщике"""
    id: int
    custom_name: Optional[str] = None
    first_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    role: str


class ProductResponse(ProductBase):
    """Схема ответа с информацией о продукте"""
    id: int = Field(..., description="ID продукта")
    supplier_user_id: int = Field(..., description="ID поставщика")
    approved_by: Optional[int] = Field(None, description="ID пользователя, который утвердил")
    approved_at: Optional[str] = Field(None, description="Дата утверждения")
    created_at: str = Field(..., description="Дата создания")
    updated_at: str = Field(..., description="Дата обновления")
    
    # Связанные объекты
    status: Optional[StatusInfo] = Field(None, description="Информация о статусе")
    category: Optional[CategoryInfo] = Field(None, description="Информация о категории")
    supplier: Optional[SupplierInfo] = Field(None, description="Информация о поставщике")
    
    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Схема ответа со списком продуктов"""
    data: list[ProductResponse] = Field(..., description="Список продуктов")
    total: int = Field(..., description="Общее количество записей")
    page: int = Field(..., description="Текущая страница")
    page_size: int = Field(..., description="Размер страницы")

