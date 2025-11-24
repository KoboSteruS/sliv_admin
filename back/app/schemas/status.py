"""
Схемы для работы со статусами
"""
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class StatusResponse(BaseModel):
    """Схема ответа с информацией о статусе"""
    id: int = Field(..., description="ID статуса")
    entity_type: Optional[str] = Field(None, description="Тип сущности")
    code: Optional[str] = Field(None, description="Код статуса")
    name: Optional[str] = Field(None, description="Название статуса")
    color: Optional[str] = Field(None, description="Цвет для отображения")
    order_index: Optional[int] = Field(None, description="Порядок сортировки")
    is_final: Optional[bool] = Field(None, description="Финальный ли статус")
    
    model_config = ConfigDict(from_attributes=True)

