"""
Сервис для работы с заявками (products)
"""
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, or_, func
from loguru import logger

from app.models.product import Product
from app.models.supplier import Supplier
from app.models.status import Status
from app.models.user_account import UserAccount
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Сервис для работы с заявками"""
    
    @staticmethod
    def get_products(
        db: Session,
        supplier_user_id: Optional[int] = None,
        status_id: Optional[int] = None,
        category_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
    ) -> tuple[list[Product], int]:
        """
        Получает список заявок с фильтрацией и пагинацией.
        
        Args:
            db: Сессия БД
            supplier_user_id: Фильтр по ID пользователя (bo.users.id), создавшего заявку
            status_id: Фильтр по ID статуса
            category_id: Фильтр по ID категории
            page: Номер страницы (начинается с 1)
            page_size: Размер страницы
            search: Поиск по названию/описанию
        
        Returns:
            Кортеж (список продуктов, общее количество)
        """
        try:
            # Базовый запрос
            query = db.query(Product)
            
            # Фильтры
            if supplier_user_id:
                query = query.filter(Product.supplier_user_id == supplier_user_id)
            
            if status_id:
                query = query.filter(Product.status_id == status_id)
            
            if category_id:
                query = query.filter(Product.category_id == category_id)
            
            if search:
                search_pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        Product.source_url.ilike(search_pattern),
                        Product.description.ilike(search_pattern),
                        Product.composition.ilike(search_pattern),
                    )
                )
            
            # Подгружаем связанные объекты для избежания N+1 проблемы
            # Используем selectinload для более эффективной загрузки
            query = query.options(
                selectinload(Product.supplier_account).selectinload(UserAccount.supplier_profile),
                selectinload(Product.status),
                selectinload(Product.category),
            )
            
            # Получаем общее количество
            total = query.count()
            
            # Применяем пагинацию
            offset = (page - 1) * page_size
            products = query.order_by(Product.created_at.desc()).offset(offset).limit(page_size).all()
            
            logger.info(f"Получено {len(products)} заявок из {total} (страница {page})")
            return products, total
            
        except Exception as e:
            logger.error(f"Ошибка при получении заявок: {e}")
            raise
    
    @staticmethod
    def get_product_by_id(
        db: Session,
        product_id: int,
        supplier_user_id: Optional[int] = None,
    ) -> Optional[Product]:
        """
        Получает заявку по ID.
        
        Args:
            db: Сессия БД
            product_id: ID заявки
            supplier_user_id: Опциональный фильтр по пользователю (bo.users.id) для проверки прав
        
        Returns:
            Product или None
        """
        try:
            query = db.query(Product).options(
                selectinload(Product.supplier_account).selectinload(UserAccount.supplier_profile),
                selectinload(Product.status),
                selectinload(Product.category),
            ).filter(Product.id == product_id)
            
            if supplier_user_id:
                query = query.filter(Product.supplier_user_id == supplier_user_id)
            
            product = query.first()
            
            if product:
                logger.info(f"Заявка {product_id} найдена")
            else:
                logger.warning(f"Заявка {product_id} не найдена")
            
            return product
            
        except Exception as e:
            logger.error(f"Ошибка при получении заявки {product_id}: {e}")
            raise
    
    @staticmethod
    def create_product(
        db: Session,
        product_data: ProductCreate,
        supplier: Optional[Supplier] = None,
    ) -> Product:
        """
        Создаёт новую заявку.
        
        Args:
            db: Сессия БД
            product_data: Данные для создания заявки
        
        Returns:
            Созданная заявка
        """
        try:
            if not product_data.supplier_user_id:
                raise ValueError("Не удалось определить пользователя поставщика для заявки")
            
            user = (
                db.query(UserAccount)
                .filter(UserAccount.id == product_data.supplier_user_id)
                .first()
            )
            if not user:
                raise ValueError(
                    f"Пользователь с ID {product_data.supplier_user_id} не найден в bo.users"
                )
            
            # Если status_id не указан, устанавливаем статус "новый" автоматически
            status_id = product_data.status_id
            if not status_id:
                new_status = db.query(Status).filter(
                    Status.entity_type == "product",
                    Status.code == "new"
                ).first()
                if new_status:
                    status_id = new_status.id
                    logger.info(f"Установлен статус 'новый' (ID: {status_id}) для новой заявки")
                else:
                    # Если статус "новый" не найден, берем первый статус для продуктов
                    first_status = db.query(Status).filter(
                        Status.entity_type == "product"
                    ).order_by(Status.order_index.asc().nullslast(), Status.id).first()
                    if first_status:
                        status_id = first_status.id
                        logger.warning(f"Статус 'новый' не найден, используется первый статус (ID: {status_id})")
                    else:
                        raise ValueError("Не найден статус для новой заявки")
            
            # Подготавливаем данные для создания продукта
            # Используем id пользователя из bo.users (не tg_user_id!)
            product_dict = product_data.model_dump(exclude_unset=True)
            product_dict["status_id"] = status_id
            product_dict["supplier_user_id"] = user.id
            
            # Создаём заявку
            product = Product(**product_dict)
            db.add(product)
            db.commit()
            db.refresh(product)
            
            supplier_name = None
            if supplier:
                supplier_name = (
                    supplier.custom_name
                    or supplier.first_name
                    or supplier.username
                    or f"SupplierID:{supplier.id}"
                )
            else:
                supplier_name = (
                    user.first_name
                    or user.username
                    or f"UserID:{user.id}"
                )
            logger.info(f"Создана заявка {product.id} для {supplier_name}")
            return product
            
        except Exception as e:
            db.rollback()
            logger.error(f"Ошибка при создании заявки: {e}")
            raise
    
    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
        supplier_user_id: Optional[int] = None,
    ) -> Optional[Product]:
        """
        Обновляет заявку.
        
        Args:
            db: Сессия БД
            product_id: ID заявки
            product_data: Данные для обновления
            supplier_user_id: Опциональный фильтр по пользователю (bo.users.id) для проверки прав
        
        Returns:
            Обновлённая заявка или None
        """
        try:
            query = db.query(Product).filter(Product.id == product_id)
            
            if supplier_user_id:
                query = query.filter(Product.supplier_user_id == supplier_user_id)
            
            product = query.first()
            
            if not product:
                logger.warning(f"Заявка {product_id} не найдена для обновления")
                return None
            
            # Обновляем поля
            update_data = product_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product, field, value)
            
            db.commit()
            db.refresh(product)
            
            logger.info(f"Заявка {product_id} обновлена")
            return product
            
        except Exception as e:
            db.rollback()
            logger.error(f"Ошибка при обновлении заявки {product_id}: {e}")
            raise
    
    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
        supplier_user_id: Optional[int] = None,
    ) -> bool:
        """
        Удаляет заявку.
        
        Args:
            db: Сессия БД
            product_id: ID заявки
            supplier_user_id: Опциональный фильтр по пользователю (bo.users.id) для проверки прав
        
        Returns:
            True если удалено, False если не найдено
        """
        try:
            query = db.query(Product).filter(Product.id == product_id)
            
            if supplier_user_id:
                query = query.filter(Product.supplier_user_id == supplier_user_id)
            
            product = query.first()
            
            if not product:
                logger.warning(f"Заявка {product_id} не найдена для удаления")
                return False
            
            db.delete(product)
            db.commit()
            
            logger.info(f"Заявка {product_id} удалена")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Ошибка при удалении заявки {product_id}: {e}")
            raise

