"""
API endpoints для работы с категориями
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryResponse

router = APIRouter()

# Простой кэш для категорий (так как они редко меняются)
_categories_cache: Optional[list[CategoryResponse]] = None
_cache_timestamp: Optional[datetime] = None
_cache_ttl = timedelta(minutes=5)  # Кэш на 5 минут


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="Получить список категорий",
    description="Возвращает список всех доступных категорий.",
)
async def get_categories(
    db: Session = Depends(get_db),
):
    """Получает список категорий (с кэшированием)"""
    global _categories_cache, _cache_timestamp
    
    # Проверяем кэш
    if _categories_cache is not None and _cache_timestamp is not None:
        if datetime.now() - _cache_timestamp < _cache_ttl:
            logger.info(f"Возвращаем категории из кэша ({len(_categories_cache)} шт.)")
            return _categories_cache
    
    try:
        logger.info("Начало запроса категорий из БД")
        categories = db.query(Category).order_by(Category.id).all()
        logger.info(f"Найдено категорий в БД: {len(categories)}")
        
        result = []
        for c in categories:
            try:
                result.append(CategoryResponse(id=c.id, name=c.name, code=c.code))
            except Exception as conv_error:
                logger.error(f"Ошибка преобразования категории {c.id}: {conv_error}, данные: id={c.id}, name={c.name}, code={c.code}")
                # Пропускаем проблемную категорию
                continue
        
        # Обновляем кэш
        _categories_cache = result
        _cache_timestamp = datetime.now()
        
        logger.info(f"Успешно возвращено категорий: {len(result)} (кэш обновлён)")
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении категорий: {e}", exc_info=True)
        
        # Если есть кэш, возвращаем его даже если он устарел
        if _categories_cache is not None:
            logger.warning(f"Используем устаревший кэш из-за ошибки БД: {e}")
            return _categories_cache
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении категорий: {str(e)}",
        )

