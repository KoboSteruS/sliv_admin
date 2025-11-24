"""
API endpoints для работы с заявками (products)
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.dependencies import require_supplier_role, get_supplier_by_token
from app.models.supplier import Supplier
from app.models.user_account import UserAccount
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    StatusInfo,
    CategoryInfo,
    SupplierInfo,
)
from app.services.product_service import ProductService

router = APIRouter()


def _product_to_response(product) -> ProductResponse:
    """Преобразует модель Product в схему ответа"""
    supplier_info = None
    supplier_account = getattr(product, "supplier_account", None)
    supplier_profile = None
    if supplier_account:
        supplier_profile = supplier_account.supplier_profile
    
    if supplier_profile:
        supplier_info = SupplierInfo(
            id=supplier_profile.id,
            custom_name=supplier_profile.custom_name,
            first_name=supplier_profile.first_name,
            username=supplier_profile.username,
            email=None,
            role=supplier_profile.role,
        )
    elif supplier_account:
        supplier_info = SupplierInfo(
            id=supplier_account.id,
            custom_name=supplier_account.first_name or supplier_account.username,
            first_name=supplier_account.first_name,
            username=supplier_account.username,
            email=supplier_account.email,
            role=supplier_account.role or "supplier",
        )

    return ProductResponse(
        id=product.id,
        source_url=product.source_url,
        price_rub=product.price_rub,
        category_id=product.category_id,
        status_id=product.status_id,
        supplier_user_id=product.supplier_user_id,
        country_of_origin=product.country_of_origin,
        composition=product.composition,
        size_range=product.size_range,
        color=product.color,
        description=product.description,
        attributes=product.attributes,
        is_active=product.is_active,
        approved_by=product.approved_by,
        approved_at=product.approved_at.isoformat() if product.approved_at else None,
        created_at=product.created_at.isoformat() if product.created_at else "",
        updated_at=product.updated_at.isoformat() if product.updated_at else "",
        status=StatusInfo(
            id=product.status.id,
            name=product.status.name,
            code=product.status.code
        ) if product.status else None,
        category=CategoryInfo(
            id=product.category.id,
            name=product.category.name,
            code=product.category.code
        ) if product.category else None,
        supplier=supplier_info,
    )


def _resolve_supplier_user_id(
    db: Session,
    supplier: Supplier,
    *,
    create_if_missing: bool = False,
) -> Optional[int]:
    if not supplier.tg_user_id:
        logger.error(
            f"У поставщика {supplier.id} отсутствует tg_user_id. Невозможно связать заявку с пользователем."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вашего аккаунта нет связанного пользователя. Обратитесь к администратору.",
        )
    
    user = (
        db.query(UserAccount)
        .filter(UserAccount.tg_user_id == supplier.tg_user_id)
        .first()
    )
    
    if user:
        return user.id
    
    if not create_if_missing:
        return None
    
    user = UserAccount(
        tg_user_id=supplier.tg_user_id,
        username=supplier.username,
        first_name=supplier.first_name,
        last_name=supplier.last_name,
        phone=supplier.phone,
        role="supplier",
        is_client=False,
        deeplink_ref=supplier.deeplink_ref,
        registered_at=supplier.registered_at or datetime.utcnow(),
    )
    db.add(user)
    db.flush()
    logger.info(f"Создан аккаунт пользователя {user.id} для поставщика {supplier.id}")
    return user.id


@router.get(
    "",
    response_model=ProductListResponse,
    summary="Получить список заявок",
    description="Возвращает список заявок с пагинацией и фильтрацией. Для поставщиков возвращает только их заявки.",
)
async def get_products(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    status_id: Optional[int] = Query(None, description="Фильтр по ID статуса"),
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    search: Optional[str] = Query(None, description="Поиск по названию/описанию"),
    supplier: Optional[Supplier] = Depends(get_supplier_by_token),
    db: Session = Depends(get_db),
):
    """
    Получает список заявок.
    Если передан токен поставщика - возвращает только его заявки.
    """
    try:
        supplier_user_id = None
        if supplier:
            supplier_user_id = _resolve_supplier_user_id(db, supplier, create_if_missing=False)
            if supplier_user_id is None:
                return ProductListResponse(data=[], total=0, page=page, page_size=page_size)
    
        products, total = ProductService.get_products(
            db=db,
            supplier_user_id=supplier_user_id,
            status_id=status_id,
            category_id=category_id,
            page=page,
            page_size=page_size,
            search=search,
        )
        
        # Преобразуем в схемы ответа
        product_responses = []
        for p in products:
            try:
                product_responses.append(_product_to_response(p))
            except Exception as conv_error:
                logger.error(f"Ошибка преобразования продукта {p.id}: {conv_error}")
                # Пропускаем проблемный продукт
                continue
        
        return ProductListResponse(
            data=product_responses,
            total=total,
            page=page,
            page_size=page_size,
        )
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка заявок: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении списка заявок",
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Получить заявку по ID",
    description="Возвращает информацию о заявке по её ID.",
)
async def get_product(
    product_id: int,
    supplier: Optional[Supplier] = Depends(get_supplier_by_token),
    db: Session = Depends(get_db),
):
    """Получает заявку по ID"""
    try:
        supplier_user_id = None
        if supplier:
            supplier_user_id = _resolve_supplier_user_id(db, supplier, create_if_missing=False)
            if supplier_user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заявка не найдена",
                )
        
        product = ProductService.get_product_by_id(
            db=db,
            product_id=product_id,
            supplier_user_id=supplier_user_id,
        )
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка не найдена",
            )
        
        return _product_to_response(product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении заявки {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении заявки",
        )


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую заявку",
    description="Создаёт новую заявку. Требуется роль 'supplier'.",
)
async def create_product(
    product_data: ProductCreate,
    supplier: Supplier = Depends(require_supplier_role),
    db: Session = Depends(get_db),
):
    """Создаёт новую заявку"""
    try:
        supplier_user_id = _resolve_supplier_user_id(db, supplier, create_if_missing=True)
        if not supplier_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось определить пользователя для поставщика",
            )
        product_data.supplier_user_id = supplier_user_id
        
        product = ProductService.create_product(
            db=db,
            product_data=product_data,
            supplier=supplier,
        )
        
        return _product_to_response(product)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Ошибка при создании заявки: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании заявки",
        )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Обновить заявку",
    description="Обновляет заявку. Поставщики могут обновлять только свои заявки.",
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    supplier: Optional[Supplier] = Depends(get_supplier_by_token),
    db: Session = Depends(get_db),
):
    """Обновляет заявку"""
    try:
        supplier_user_id = None
        if supplier:
            supplier_user_id = _resolve_supplier_user_id(db, supplier, create_if_missing=False)
            if supplier_user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заявка не найдена или нет прав на её изменение",
                )
        
        product = ProductService.update_product(
            db=db,
            product_id=product_id,
            product_data=product_data,
            supplier_user_id=supplier_user_id,
        )
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка не найдена или нет прав на её изменение",
            )
        
        return _product_to_response(product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обновлении заявки {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении заявки",
        )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить заявку",
    description="Удаляет заявку. Поставщики могут удалять только свои заявки.",
)
async def delete_product(
    product_id: int,
    supplier: Optional[Supplier] = Depends(get_supplier_by_token),
    db: Session = Depends(get_db),
):
    """Удаляет заявку"""
    try:
        supplier_user_id = None
        if supplier:
            supplier_user_id = _resolve_supplier_user_id(db, supplier, create_if_missing=False)
            if supplier_user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заявка не найдена или нет прав на её удаление",
                )
        
        deleted = ProductService.delete_product(
            db=db,
            product_id=product_id,
            supplier_user_id=supplier_user_id,
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка не найдена или нет прав на её удаление",
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при удалении заявки {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении заявки",
        )

