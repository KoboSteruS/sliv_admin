"""
Pydantic схемы для валидации данных
"""
from app.schemas.product import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from app.schemas.supplier import SupplierResponse
from app.schemas.status import StatusResponse
from app.schemas.category import CategoryResponse

__all__ = [
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductListResponse",
    "SupplierResponse",
    "StatusResponse",
    "CategoryResponse",
]

