# Sliv Admin - Админ-панель для управления заявками

## Описание проекта

Админ-панель для управления заявками поставщиков. Состоит из двух частей:
- **Frontend** (Refine + React + TypeScript) - админ-панель
- **Backend** (FastAPI + Python) - REST API для работы с PostgreSQL

## Структура проекта

```
Sliv_Admin/
├── back/                    # Backend API (FastAPI)
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── services/       # Бизнес-логика
│   │   └── main.py         # Точка входа
│   └── requirements.txt
└── wild-camels-nail/       # Frontend (Refine)
    ├── src/
    │   ├── pages/          # Страницы приложения
    │   ├── components/     # Компоненты UI
    │   └── providers/      # Провайдеры (dataProvider)
    └── package.json
```

## Быстрый старт

### Backend

1. Перейди в папку `back`:
```bash
cd back
```

2. Создай виртуальное окружение:
```bash
python -m venv venv
```

3. Активируй виртуальное окружение:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Установи зависимости:
```bash
pip install -r requirements.txt
```

5. Создай файл `.env` (опционально, значения по умолчанию уже настроены):
```env
DATABASE_URL=postgresql://sliv_test_user:sFSfj9wp2@10.10.10.11:5432/sliv_test
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

6. Запусти сервер:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен по адресу: `http://localhost:8000`
Документация: `http://localhost:8000/docs`

### Frontend

1. Перейди в папку `wild-camels-nail`:
```bash
cd wild-camels-nail
```

2. Установи зависимости:
```bash
npm install
```

3. Создай файл `.env` (опционально):
```env
VITE_API_URL=http://localhost:8000/api/v1
```

4. Запусти dev-сервер:
```bash
npm run dev
```

Приложение будет доступно по адресу: `http://localhost:5173`

## Использование

### Доступ по токену

Токен передаётся через query параметр в URL:
```
http://localhost:5173/products?token=YOUR_TOKEN_HERE
```

Токен автоматически добавляется ко всем API запросам.

### Страница "Заявки"

Для пользователей с ролью `supplier` доступна страница "Заявки" (`/products`), где:
- Отображается список текущих заявок
- Есть кнопка "Создать новую заявку"
- Можно редактировать и просматривать заявки
- Доступны фильтры по статусу и категории

## API Endpoints

### Products (Заявки)

- `GET /api/v1/products` - Список заявок (с пагинацией и фильтрацией)
- `GET /api/v1/products/{id}` - Получить заявку по ID
- `POST /api/v1/products` - Создать новую заявку
- `PUT /api/v1/products/{id}` - Обновить заявку
- `DELETE /api/v1/products/{id}` - Удалить заявку

### Statuses (Статусы)

- `GET /api/v1/statuses` - Список статусов

### Categories (Категории)

- `GET /api/v1/categories` - Список категорий

Все endpoints поддерживают передачу токена через query параметр `?token=...`

## База данных

Подключение к PostgreSQL:
- Хост: `10.10.10.11`
- База данных: `sliv_test`
- Пользователь: `sliv_test_user`
- Пароль: `sFSfj9wp2`

### Таблицы

- `suppliers` - Поставщики (пользователи с токенами)
- `products` - Заявки/товары
- `statuses` - Статусы заявок
- `categories` - Категории товаров

## Технологии

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL (psycopg2)
- Pydantic
- Loguru

### Frontend
- Refine
- React 19
- TypeScript
- Vite
- shadcn/ui
- TanStack Table

## Разработка

### Структура кода

Код следует принципам:
- SOLID
- DRY
- Модульность и поддерживаемость
- Обработка ошибок
- Типизация (TypeScript/Python)

### Логирование

Backend использует `loguru` для логирования. Логи сохраняются в `back/logs/app.log`.

## TODO

- [x] Создать структуру backend API
- [x] Настроить подключение к PostgreSQL
- [x] Создать API endpoints для заявок
- [x] Настроить авторизацию по токену
- [x] Создать страницу "Заявки" на фронтенде
- [x] Настроить dataProvider с поддержкой токена
- [ ] Добавить валидацию форм
- [ ] Добавить обработку ошибок на фронтенде
- [ ] Добавить фильтры и поиск в таблице заявок

## Лицензия

Проект для внутреннего использования.

