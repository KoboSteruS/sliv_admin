"""
Скрипт для проверки работы API
Запусти: python check_api.py
Убедись, что сервер запущен на http://localhost:8000
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Проверка работы API")
print("=" * 60)

# 1. Health check
print("\n1. Health check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
    if response.status_code == 200:
        print("   ✅ API работает!")
    else:
        print("   ⚠️  Неожиданный статус")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    print("   Убедись, что сервер запущен: python -m uvicorn app.main:app --reload --port 8000")
    exit(1)

# 2. Главная страница
print("\n2. Главная страница...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 3. Список заявок (без токена)
print("\n3. GET /api/v1/products (без токена)...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/products", timeout=10)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Всего заявок: {data.get('total', 0)}")
        print(f"   На странице: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"   Первая заявка: {json.dumps(data['data'][0], indent=2, ensure_ascii=False)}")
    else:
        print(f"   Ответ: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 4. Список статусов
print("\n4. GET /api/v1/statuses...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/statuses", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Найдено статусов: {len(data)}")
        for status in data[:5]:
            print(f"   - {status}")
    else:
        print(f"   Ответ: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 5. Список категорий
print("\n5. GET /api/v1/categories...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/categories", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Найдено категорий: {len(data)}")
        for category in data[:5]:
            print(f"   - {category}")
    else:
        print(f"   Ответ: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 6. Документация
print("\n6. Документация API...")
print(f"   Swagger UI: {BASE_URL}/docs")
print(f"   ReDoc: {BASE_URL}/redoc")

print("\n" + "=" * 60)
print("✅ Проверка API завершена!")
print("=" * 60)

