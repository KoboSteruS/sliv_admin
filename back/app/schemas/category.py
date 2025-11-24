"""
Схемы для работы с категориями
"""
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class CategoryResponse(BaseModel):
    """Схема ответа с информацией о категории"""
    id: int = Field(..., description="ID категории")
    code: Optional[str] = Field(None, description="Код категории")
    name: Optional[str] = Field(None, description="Название категории")
    required_fields: Optional[list[Any]] = Field(None, description="Обязательные поля")
    
    model_config = ConfigDict(from_attributes=True)

