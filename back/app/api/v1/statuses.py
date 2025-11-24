"""
API endpoints для работы со статусами
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.models.status import Status
from app.schemas.status import StatusResponse

router = APIRouter()


@router.get(
    "",
    response_model=list[StatusResponse],
    summary="Получить список статусов",
    description="Возвращает список всех доступных статусов для продуктов.",
)
async def get_statuses(
    entity_type: Optional[str] = Query("product", description="Тип сущности (product, etc)"),
    db: Session = Depends(get_db),
):
    """Получает список статусов"""
    try:
        query = db.query(Status)
        
        # Фильтруем по типу сущности (по умолчанию product)
        if entity_type:
            query = query.filter(Status.entity_type == entity_type)
        
        statuses = query.order_by(Status.order_index.asc().nullslast(), Status.id).all()
        
        return [
            StatusResponse(
                id=s.id,
                entity_type=s.entity_type,
                code=s.code,
                name=s.name,
                color=s.color,
                order_index=s.order_index,
                is_final=s.is_final,
            )
            for s in statuses
        ]
    except Exception as e:
        logger.error(f"Ошибка при получении статусов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении статусов",
        )

