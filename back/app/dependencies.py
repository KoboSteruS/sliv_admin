"""
Зависимости для FastAPI (JWT, токены, авторизация)
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.models.supplier import Supplier


def get_supplier_by_token(
    token: Optional[str] = Query(None, description="Токен для доступа"),
    db: Session = Depends(get_db),
) -> Optional[Supplier]:
    """
    Получает поставщика по токену из query параметра.
    Если токен не передан или не найден - возвращает None.
    """
    if not token:
        logger.warning("Токен не передан в запросе")
        return None
    
    try:
        supplier = db.query(Supplier).filter(Supplier.token == token).first()
        if not supplier:
            logger.warning(f"Поставщик с токеном {token[:10]}... не найден")
            return None
        
        # Получаем имя поставщика для логирования
        supplier_name = (
            supplier.custom_name or 
            supplier.first_name or 
            supplier.username or 
            f"ID:{supplier.id}"
        )
        logger.info(f"Поставщик {supplier_name} (ID: {supplier.id}) авторизован по токену")
        return supplier
    except Exception as e:
        logger.error(f"Ошибка при проверке токена: {e}")
        return None


def require_supplier(
    supplier: Optional[Supplier] = Depends(get_supplier_by_token),
) -> Supplier:
    """
    Требует наличие валидного токена и возвращает поставщика.
    Вызывает 401 если токен невалиден или отсутствует.
    """
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не предоставлен или невалиден",
        )
    
    return supplier


def require_supplier_role(
    supplier: Supplier = Depends(require_supplier),
) -> Supplier:
    """
    Требует роль 'supplier' у пользователя.
    """
    if supplier.role != "supplier":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён. Требуется роль 'supplier'",
        )
    
    return supplier

