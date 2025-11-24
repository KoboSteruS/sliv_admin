"""
Схемы для работы с поставщиками
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SupplierResponse(BaseModel):
    """Схема ответа с информацией о поставщике"""
    id: int = Field(..., description="ID поставщика")
    tg_user_id: Optional[int] = Field(None, description="Telegram user ID")
    phone: Optional[str] = Field(None, description="Телефон")
    email: Optional[str] = Field(None, description="Email")
    username: Optional[str] = Field(None, description="Username")
    first_name: Optional[str] = Field(None, description="Имя")
    last_name: Optional[str] = Field(None, description="Фамилия")
    custom_name: Optional[str] = Field(None, description="Кастомное имя")
    role: str = Field(..., description="Роль пользователя")
    
    model_config = ConfigDict(from_attributes=True)
    
    @property
    def name(self) -> str:
        """Возвращает имя поставщика"""
        return self.custom_name or self.first_name or self.username or f"ID:{self.id}"

