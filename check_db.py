"""
Скрипт для проверки подключения к БД
Запусти: python check_db.py
"""
import sys
sys.path.insert(0, 'back')

print("=" * 60)
print("Проверка подключения к PostgreSQL")
print("=" * 60)

try:
    from app.database import engine
    from sqlalchemy import text
    
    print("\n1. Подключение к БД...")
    with engine.connect() as conn:
        # Проверка версии PostgreSQL
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"   ✅ Подключено!")
        print(f"   PostgreSQL: {version.split(',')[0]}")
        
        # Проверка таблиц
        print("\n2. Проверка таблиц...")
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"   Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"   - {table}")
        
        # Проверка нужных таблиц
        required = ['suppliers', 'products', 'statuses', 'categories']
        missing = [t for t in required if t not in tables]
        
        if missing:
            print(f"\n   ⚠️  Отсутствуют: {missing}")
        else:
            print(f"\n   ✅ Все необходимые таблицы найдены!")
        
        # Структура products
        if 'products' in tables:
            print("\n3. Структура таблицы products:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_name = 'products'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                default = f" DEFAULT {row[3]}" if row[3] else ""
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"   - {row[0]}: {row[1]} {nullable}{default}")
            
            # Количество записей
            result = conn.execute(text("SELECT COUNT(*) FROM products;"))
            count = result.fetchone()[0]
            print(f"\n   Количество заявок: {count}")
        
        # Структура suppliers
        if 'suppliers' in tables:
            print("\n4. Структура таблицы suppliers:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable
                FROM information_schema.columns
                WHERE table_name = 'suppliers'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"   - {row[0]}: {row[1]} {nullable}")
            
            # Количество записей
            result = conn.execute(text("SELECT COUNT(*) FROM suppliers;"))
            count = result.fetchone()[0]
            print(f"\n   Количество поставщиков: {count}")
        
        # Структура statuses
        if 'statuses' in tables:
            print("\n5. Структура таблицы statuses:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type
                FROM information_schema.columns
                WHERE table_name = 'statuses'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                print(f"   - {row[0]}: {row[1]}")
            
            # Данные
            result = conn.execute(text("SELECT * FROM statuses LIMIT 10;"))
            rows = result.fetchall()
            if rows:
                print(f"\n   Данные (первые {len(rows)} записей):")
                for row in rows:
                    print(f"   - {row}")
        
        # Структура categories
        if 'categories' in tables:
            print("\n6. Структура таблицы categories:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type
                FROM information_schema.columns
                WHERE table_name = 'categories'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                print(f"   - {row[0]}: {row[1]}")
            
            # Данные
            result = conn.execute(text("SELECT * FROM categories LIMIT 10;"))
            rows = result.fetchall()
            if rows:
                print(f"\n   Данные (первые {len(rows)} записей):")
                for row in rows:
                    print(f"   - {row}")
    
    print("\n" + "=" * 60)
    print("✅ Проверка завершена успешно!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    print("\nДетали ошибки:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

