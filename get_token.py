"""
Скрипт для получения токена из таблицы suppliers
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Параметры подключения
DB_CONFIG = {
    "host": "10.10.10.11",
    "database": "sliv_test",
    "user": "sliv_test_user",
    "password": "sFSfj9wp2",
    "port": 5432,
}

print("=" * 60)
print("Получение токенов из таблицы suppliers")
print("=" * 60)

try:
    # Подключаемся к БД
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Получаем всех поставщиков с токенами
    cursor.execute("""
        SELECT 
            id,
            tg_user_id,
            username,
            first_name,
            custom_name,
            role,
            token,
            registered_at
        FROM bo.suppliers
        WHERE token IS NOT NULL
        ORDER BY registered_at DESC
        LIMIT 10
    """)
    
    suppliers = cursor.fetchall()
    
    if not suppliers:
        print("\n❌ Токены не найдены в таблице suppliers")
    else:
        print(f"\n✅ Найдено поставщиков с токенами: {len(suppliers)}\n")
        
        for i, supplier in enumerate(suppliers, 1):
            print(f"{i}. Поставщик ID: {supplier['id']}")
            print(f"   Username: {supplier.get('username') or 'N/A'}")
            print(f"   Имя: {supplier.get('first_name') or supplier.get('custom_name') or 'N/A'}")
            print(f"   Роль: {supplier.get('role', 'N/A')}")
            print(f"   Токен: {supplier['token']}")
            print(f"   Зарегистрирован: {supplier.get('registered_at')}")
            print()
        
        # Берем первый токен для тестов
        test_token = suppliers[0]['token']
        print("=" * 60)
        print("Токен для тестирования:")
        print("=" * 60)
        print(f"\n{test_token}\n")
        print("=" * 60)
        print("\nИспользование:")
        print(f"1. Открой в браузере: http://localhost:5173/?token={test_token}")
        print(f"2. Или добавь в URL при запросах: ?token={test_token}")
        print("=" * 60)
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"\n❌ Ошибка подключения к БД: {e}")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")

