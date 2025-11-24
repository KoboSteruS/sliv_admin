"""
Простой тест подключения к БД
"""
import sys
sys.path.insert(0, 'back')

from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ Подключение к БД успешно!")
        print(f"PostgreSQL версия: {version[:50]}...")
        
        # Проверяем таблицы
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"\n📋 Найденные таблицы ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
        
        # Проверяем нужные таблицы
        required = ['suppliers', 'products', 'statuses', 'categories']
        missing = [t for t in required if t not in tables]
        
        if missing:
            print(f"\n⚠️  Отсутствующие таблицы: {missing}")
        else:
            print(f"\n✅ Все необходимые таблицы найдены!")
        
        # Проверяем структуру таблицы products
        if 'products' in tables:
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'products'
                ORDER BY ordinal_position;
            """))
            print(f"\n📊 Структура таблицы products:")
            for row in result.fetchall():
                print(f"  - {row[0]}: {row[1]} (nullable: {row[2]})")
            
            result = conn.execute(text("SELECT COUNT(*) FROM products;"))
            count = result.fetchone()[0]
            print(f"\n📊 Количество заявок в products: {count}")
            
        # Проверяем структуру suppliers
        if 'suppliers' in tables:
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'suppliers'
                ORDER BY ordinal_position;
            """))
            print(f"\n👤 Структура таблицы suppliers:")
            for row in result.fetchall():
                print(f"  - {row[0]}: {row[1]} (nullable: {row[2]})")
            
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    import traceback
    traceback.print_exc()

