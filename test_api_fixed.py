"""
Тест API после исправления моделей
Запусти: python test_api_fixed.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Тест API после исправления моделей")
print("=" * 60)

# 1. Health check
print("\n1. Health check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ API работает!")
    else:
        print(f"   Ответ: {response.text}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    exit(1)

# 2. Список заявок (без токена)
print("\n2. GET /api/v1/products (без токена)...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/products?page=1&page_size=10", timeout=10)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Всего заявок: {data.get('total', 0)}")
        print(f"   На странице: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"\n   Первая заявка:")
            first = data['data'][0]
            print(f"   - ID: {first.get('id')}")
            print(f"   - URL: {first.get('source_url', 'N/A')}")
            print(f"   - Цена: {first.get('price_rub', 'N/A')} руб")
            print(f"   - Статус: {first.get('status', {}).get('name', 'N/A')}")
            print(f"   - Категория: {first.get('category', {}).get('name', 'N/A')}")
    else:
        print(f"   ❌ Ошибка: {response.text[:500]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 3. Список статусов
print("\n3. GET /api/v1/statuses...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/statuses", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Найдено статусов: {len(data)}")
        for status in data[:5]:
            print(f"   - {status.get('name', 'N/A')} (код: {status.get('code', 'N/A')})")
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
        print(f"   ✅ Успешно!")
        print(f"   Найдено категорий: {len(data)}")
        for category in data[:5]:
            print(f"   - {category.get('name', 'N/A')} (код: {category.get('code', 'N/A')})")
    else:
        print(f"   ❌ Ошибка: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n" + "=" * 60)
print("✅ Тест завершён!")
print("=" * 60)

