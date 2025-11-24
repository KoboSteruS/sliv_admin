"""
Скрипт для отображения структуры таблиц в схеме PostgreSQL.

Пример:
    python check_table_structure.py --tables products suppliers statuses categories users
"""

import argparse
from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    "host": "10.10.10.11",
    "port": 5432,
    "dbname": "sliv_test",
    "user": "sliv_test_user",
    "password": "sFSfj9wp2",
    "connect_timeout": 10,
}

DEFAULT_TABLES = ["products", "suppliers", "statuses", "categories", "users"]


def fetch_table_info(cursor, schema: str, table: str) -> List[dict]:
    cursor.execute(
        """
        SELECT
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """,
        (schema, table),
    )
    return cursor.fetchall()


def fetch_row_count(cursor, schema: str, table: str) -> int:
    cursor.execute(f'SELECT COUNT(*) AS count FROM "{schema}"."{table}"')
    row = cursor.fetchone()
    if row is None:
        return 0
    if isinstance(row, dict):
        return row.get("count", 0)
    # row is a tuple
    return row[0]


def print_table_structure(cursor, schema: str, table: str) -> None:
    print("=" * 70)
    print(f"Таблица: {schema}.{table}")
    print("=" * 70)

    try:
        columns = fetch_table_info(cursor, schema, table)
        count = fetch_row_count(cursor, schema, table)
    except Exception as exc:
        print(f"❌ Ошибка при получении данных ({type(exc).__name__}): {exc}")
        return

    if not columns:
        print("⚠️  Колонки не найдены (возможно, таблица отсутствует).")
        return

    print(f"Количество записей: {count}")
    print("-" * 70)
    print(f"{'Имя колонки':25} | {'Тип':20} | {'Null?':6} | Значение по умолчанию")
    print("-" * 70)
    for col in columns:
        default = col["column_default"] or ""
        print(
            f"{col['column_name']:25} | {col['data_type']:20} | "
            f"{col['is_nullable']:6} | {default}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Показать структуру таблиц PostgreSQL (Схема по умолчанию 'bo')."
    )
    parser.add_argument(
        "--schema",
        default="bo",
        help="Имя схемы (default: bo)",
    )
    parser.add_argument(
        "--tables",
        nargs="+",
        default=DEFAULT_TABLES,
        help="Список таблиц (default: products suppliers statuses categories users)",
    )

    args = parser.parse_args()

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            conn.autocommit = True
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                for table in args.tables:
                    print_table_structure(cursor, args.schema, table)
    except Exception as exc:
        print(f"❌ Ошибка подключения или выполнения запроса ({type(exc).__name__}): {exc}")


if __name__ == "__main__":
    main()


