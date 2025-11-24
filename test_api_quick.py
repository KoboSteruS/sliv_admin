"""
Быстрый тест API с увеличенным timeout
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Быстрый тест API")
print("=" * 60)

# 1. Health check
print("\n1. Health check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   ✅ Статус: {response.status_code}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    exit(1)

# 2. Список заявок (без токена, с коротким timeout)
print("\n2. GET /api/v1/products (timeout=30)...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/products?page=1&page_size=10", timeout=30)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Всего заявок: {data.get('total', 0)}")
        print(f"   На странице: {len(data.get('data', []))}")
    else:
        print(f"   ❌ Ошибка: {response.text[:500]}")
except requests.exceptions.Timeout:
    print("   ⚠️  Timeout - запрос выполняется слишком долго")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 3. Список статусов (только для продуктов)
print("\n3. GET /api/v1/statuses?entity_type=product...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/statuses?entity_type=product", timeout=10)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Найдено статусов: {len(data)}")
        for s in data[:5]:
            print(f"   - {s.get('name', 'N/A')} (код: {s.get('code', 'N/A')})")
    else:
        print(f"   ❌ Ошибка: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 4. Список категорий
print("\n4. GET /api/v1/categories...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/categories", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно! Найдено: {len(data)}")
    else:
        print(f"   ❌ Ошибка: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n" + "=" * 60)
print("✅ Тест завершён!")
print("=" * 60)

