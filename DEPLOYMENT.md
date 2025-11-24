# Инструкция по развертыванию на сервере

## Проблема: ERR_CONNECTION_REFUSED

Если видишь ошибку `ERR_CONNECTION_REFUSED` при попытке авторизации, проверь следующее:

### 1. Проверь, что бэкенд запущен

```bash
# Проверь статус сервиса
sudo systemctl status sliv-admin-backend

# Если не запущен, запусти
sudo systemctl start sliv-admin-backend

# Проверь логи
sudo journalctl -u sliv-admin-backend -f
```

### 2. Проверь, что бэкенд слушает на правильном порту

```bash
# Проверь, что порт 8100 открыт и слушается
sudo netstat -tlnp | grep 8100
# или
sudo ss -tlnp | grep 8100
```

### 3. Проверь Nginx конфигурацию

```bash
# Проверь конфигурацию Nginx
sudo nginx -t

# Перезагрузи Nginx
sudo systemctl reload nginx

# Проверь логи Nginx
sudo tail -f /var/log/nginx/sliv-admin-error.log
```

### 4. Проверь, что фронтенд собран с правильными настройками

После изменений в коде нужно пересобрать фронтенд:

```bash
cd /root/sliv_admin/wild-camels-nail

# Если используешь .env файл, создай его:
echo "VITE_API_URL=/api/v1" > .env

# Пересобери проект
npm run build
```

### 5. Получи правильный токен из базы данных

Токен должен быть из таблицы `bo.suppliers`, а не JWT токен.

```bash
# Подключись к БД и получи токен
psql -h 10.10.10.11 -U sliv_test_user -d sliv_test -c "SELECT id, token, custom_name FROM bo.suppliers WHERE token IS NOT NULL LIMIT 5;"
```

Или используй Python скрипт:

```bash
cd /root/sliv_admin
python3 -c "
import psycopg2
conn = psycopg2.connect(host='10.10.10.11', dbname='sliv_test', user='sliv_test_user', password='sFSfj9wp2')
cur = conn.cursor()
cur.execute('SET search_path TO bo')
cur.execute('SELECT id, token, custom_name FROM suppliers WHERE token IS NOT NULL LIMIT 5')
for row in cur.fetchall():
    print(f'ID: {row[0]}, Token: {row[1]}, Name: {row[2]}')
cur.close()
conn.close()
"
```

### 6. Проверь доступность API напрямую

```bash
# Проверь health check
curl http://localhost:8100/health

# Проверь через Nginx
curl http://localhost/api/v1/health

# Проверь с токеном (замени TOKEN на реальный токен)
curl "http://localhost/api/v1/products?token=TOKEN&page=1&page_size=1"
```

### 7. Проверь CORS настройки в бэкенде

В файле `/root/sliv_admin/back/app/config.py` убедись, что в `CORS_ORIGINS` добавлен домен/IP сервера:

```python
CORS_ORIGINS: list[str] = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://your-server-ip",  # Добавь IP или домен сервера
]
```

После изменения перезапусти бэкенд:

```bash
sudo systemctl restart sliv-admin-backend
```

## Быстрая проверка всех компонентов

```bash
# 1. Бэкенд
sudo systemctl status sliv-admin-backend
curl http://localhost:8100/health

# 2. Nginx
sudo systemctl status nginx
curl http://localhost/api/v1/health

# 3. Фронтенд (если используешь dev режим)
sudo systemctl status sliv-admin-frontend

# 4. Проверь логи
sudo journalctl -u sliv-admin-backend -n 50
sudo tail -n 50 /var/log/nginx/sliv-admin-error.log
```

## Решение проблем

### Бэкенд не запускается

```bash
# Проверь логи
sudo journalctl -u sliv-admin-backend -n 100

# Проверь виртуальное окружение
cd /root/sliv_admin/back
source venv/bin/activate
python -c "import uvicorn; print('OK')"

# Попробуй запустить вручную
cd /root/sliv_admin/back
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8100
```

### Nginx возвращает 502 Bad Gateway

Это означает, что Nginx не может подключиться к бэкенду. Проверь:
1. Бэкенд запущен на порту 8100
2. В Nginx конфиге правильный адрес: `proxy_pass http://127.0.0.1:8100;`

### Фронтенд не загружается

1. Проверь, что файлы собраны: `ls -la /root/sliv_admin/wild-camels-nail/dist`
2. Проверь права доступа: `sudo chown -R www-data:www-data /root/sliv_admin/wild-camels-nail/dist`
3. Проверь Nginx конфиг - путь к `root` должен быть правильным

