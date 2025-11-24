"""
Тест подключения фронтенда к бэку
Проверяет, что фронт может достучаться до нашего API
"""
import requests

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

print("=" * 60)
print("Тест подключения фронтенда к бэку")
print("=" * 60)

# 1. Проверка бэка
print("\n1. Проверка backend API...")
try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=30)
    print(f"   ✅ Backend работает! Статус: {response.status_code}")
    print(f"   Ответ: {response.json()}")
except requests.exceptions.Timeout:
    print(f"   ❌ Timeout при подключении к {BACKEND_URL}/health")
    print("   Проверь, что backend действительно запущен и отвечает")
    print("   Попробуй открыть в браузере: http://localhost:8000/health")
except requests.exceptions.ConnectionError as e:
    print(f"   ❌ Не удалось подключиться: {e}")
    print("   Убедись, что backend запущен на порту 8000")
    print("   Проверь команду: netstat -an | findstr :8000")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    print(f"   Тип ошибки: {type(e).__name__}")

# 2. Проверка products endpoint
print("\n2. Проверка GET /api/v1/products...")
try:
    response = requests.get(f"{BACKEND_URL}/api/v1/products?page=1&page_size=10", timeout=10)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Формат ответа: {type(data)}")
        if isinstance(data, dict):
            print(f"   - data: {type(data.get('data'))}, длина: {len(data.get('data', []))}")
            print(f"   - total: {data.get('total')}")
        elif isinstance(data, list):
            print(f"   - массив, длина: {len(data)}")
    else:
        print(f"   ❌ Ошибка: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 3. Проверка statuses endpoint
print("\n3. Проверка GET /api/v1/statuses?entity_type=product...")
try:
    response = requests.get(f"{BACKEND_URL}/api/v1/statuses?entity_type=product", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Формат ответа: {type(data)}")
        if isinstance(data, list):
            print(f"   - массив, длина: {len(data)}")
            if data:
                print(f"   - первый элемент: {data[0]}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 4. Проверка categories endpoint
print("\n4. Проверка GET /api/v1/categories...")
try:
    response = requests.get(f"{BACKEND_URL}/api/v1/categories", timeout=5)
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Успешно!")
        print(f"   Формат ответа: {type(data)}")
        if isinstance(data, list):
            print(f"   - массив, длина: {len(data)}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# 5. Проверка CORS
print("\n5. Проверка CORS заголовков...")
try:
    response = requests.options(
        f"{BACKEND_URL}/api/v1/products",
        headers={
            "Origin": FRONTEND_URL,
            "Access-Control-Request-Method": "GET",
        },
        timeout=5
    )
    print(f"   Статус OPTIONS: {response.status_code}")
    cors_headers = {
        k: v for k, v in response.headers.items() 
        if k.lower().startswith("access-control")
    }
    if cors_headers:
        print(f"   ✅ CORS заголовки присутствуют:")
        for k, v in cors_headers.items():
            print(f"   - {k}: {v}")
    else:
        print(f"   ⚠️  CORS заголовки не найдены")
except Exception as e:
    print(f"   ⚠️  Не удалось проверить CORS: {e}")

print("\n" + "=" * 60)
print("✅ Тест завершён!")
print("=" * 60)
print("\nЕсли backend работает, но фронт не видит данные:")
print("1. Проверь консоль браузера - должны быть логи [DataProvider]")
print("2. Проверь Network tab в DevTools - должны быть запросы к localhost:8000")
print("3. Убедись, что нет ошибок CORS")

