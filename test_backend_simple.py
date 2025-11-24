"""
Простой тест бэкенда
"""
import requests
import time

print("Тестирую бэкенд...")
print("=" * 60)

# Тест 1: Health check
print("\n1. GET /health")
try:
    start = time.time()
    response = requests.get("http://localhost:8000/health", timeout=30)
    elapsed = time.time() - start
    print(f"   ✅ Статус: {response.status_code}")
    print(f"   ✅ Ответ: {response.json()}")
    print(f"   ✅ Время ответа: {elapsed:.2f} сек")
except requests.exceptions.Timeout:
    print("   ❌ TIMEOUT - бэкенд не отвечает за 30 секунд")
    print("   Возможно, бэкенд зависает при обработке запросов")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# Тест 2: Root endpoint
print("\n2. GET /")
try:
    start = time.time()
    response = requests.get("http://localhost:8000/", timeout=30)
    elapsed = time.time() - start
    print(f"   ✅ Статус: {response.status_code}")
    print(f"   ✅ Ответ: {response.json()}")
    print(f"   ✅ Время ответа: {elapsed:.2f} сек")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# Тест 3: Products endpoint
print("\n3. GET /api/v1/products")
try:
    start = time.time()
    response = requests.get("http://localhost:8000/api/v1/products?page=1&page_size=10", timeout=30)
    elapsed = time.time() - start
    print(f"   ✅ Статус: {response.status_code}")
    print(f"   ✅ Время ответа: {elapsed:.2f} сек")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Формат: {type(data)}")
        if isinstance(data, dict):
            print(f"   ✅ data: {len(data.get('data', []))} элементов")
            print(f"   ✅ total: {data.get('total')}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n" + "=" * 60)

