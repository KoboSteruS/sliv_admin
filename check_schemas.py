"""
Проверка схем и таблиц в БД
Запусти: python check_schemas.py
"""
import sys
sys.path.insert(0, 'back')

print("=" * 60)
print("Проверка схем и таблиц в PostgreSQL")
print("=" * 60)

try:
    from app.database import engine
    from sqlalchemy import text
    
    with engine.connect() as conn:
        # 1. Проверяем все схемы
        print("\n1. Список всех схем в БД:")
        result = conn.execute(text("""
            SELECT schema_name 
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name;
        """))
        schemas = [row[0] for row in result.fetchall()]
        for schema in schemas:
            print(f"   - {schema}")
        
        # 2. Проверяем таблицы в схеме public
        print("\n2. Таблицы в схеме 'public':")
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        public_tables = [row[0] for row in result.fetchall()]
        if public_tables:
            for table in public_tables:
                print(f"   - {table}")
        else:
            print("   (пусто)")
        
        # 3. Проверяем таблицы в схеме bo
        print("\n3. Таблицы в схеме 'bo':")
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'bo'
            ORDER BY table_name;
        """))
        bo_tables = [row[0] for row in result.fetchall()]
        if bo_tables:
            for table in bo_tables:
                print(f"   - {table}")
        else:
            print("   (пусто)")
        
        # 4. Проверяем нужные таблицы в схеме bo
        required = ['suppliers', 'products', 'statuses', 'categories']
        print("\n4. Проверка нужных таблиц в схеме 'bo':")
        for table in required:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = 'bo' AND table_name = :table_name
                );
            """), {"table_name": table})
            exists = result.fetchone()[0]
            status = "✅" if exists else "❌"
            print(f"   {status} {table}")
        
        # 5. Структура products в схеме bo
        if 'products' in bo_tables:
            print("\n5. Структура таблицы bo.products:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'bo' AND table_name = 'products'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                col_name, data_type, max_len, nullable, default = row
                length = f"({max_len})" if max_len else ""
                nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
                default_str = f" DEFAULT {default}" if default else ""
                print(f"   - {col_name}: {data_type}{length} {nullable_str}{default_str}")
            
            # Количество записей
            result = conn.execute(text('SELECT COUNT(*) FROM "bo"."products";'))
            count = result.fetchone()[0]
            print(f"\n   Количество записей: {count}")
        
        # 6. Структура suppliers в схеме bo
        if 'suppliers' in bo_tables:
            print("\n6. Структура таблицы bo.suppliers:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type,
                    character_maximum_length,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'bo' AND table_name = 'suppliers'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                col_name, data_type, max_len, nullable = row
                length = f"({max_len})" if max_len else ""
                nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"   - {col_name}: {data_type}{length} {nullable_str}")
        
        # 7. Структура statuses в схеме bo
        if 'statuses' in bo_tables:
            print("\n7. Структура таблицы bo.statuses:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type
                FROM information_schema.columns
                WHERE table_schema = 'bo' AND table_name = 'statuses'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                print(f"   - {row[0]}: {row[1]}")
            
            # Данные
            result = conn.execute(text('SELECT * FROM "bo"."statuses" LIMIT 10;'))
            rows = result.fetchall()
            if rows:
                print(f"\n   Данные (первые {len(rows)} записей):")
                for row in rows:
                    print(f"   - {row}")
        
        # 8. Структура categories в схеме bo
        if 'categories' in bo_tables:
            print("\n8. Структура таблицы bo.categories:")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type
                FROM information_schema.columns
                WHERE table_schema = 'bo' AND table_name = 'categories'
                ORDER BY ordinal_position;
            """))
            for row in result.fetchall():
                print(f"   - {row[0]}: {row[1]}")
            
            # Данные
            result = conn.execute(text('SELECT * FROM "bo"."categories" LIMIT 10;'))
            rows = result.fetchall()
            if rows:
                print(f"\n   Данные (первые {len(rows)} записей):")
                for row in rows:
                    print(f"   - {row}")
    
    print("\n" + "=" * 60)
    print("✅ Проверка завершена!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    print("\nДетали ошибки:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

