# Backend API для админ-панели Sliv

## Описание

Backend API на FastAPI для работы с PostgreSQL базой данных. Предоставляет REST API для управления заявками (products), поставщиками (suppliers), статусами и категориями.

## Установка

1. Создай виртуальное окружение:
```bash
python -m venv venv
```

2. Активируй виртуальное окружение:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Установи зависимости:
```bash
pip install -r requirements.txt
```

## Настройка

Создай файл `.env` в корне папки `back`:

```env
DATABASE_URL=postgresql://sliv_test_user:sFSfj9wp2@10.10.10.11:5432/sliv_test
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Запуск

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен по адресу: `http://localhost:8000`

Документация API: `http://localhost:8000/docs`

## Структура проекта

```
back/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа приложения
│   ├── config.py            # Конфигурация приложения
│   ├── database.py          # Подключение к БД
│   ├── dependencies.py      # Зависимости (JWT, токены)
│   ├── models/              # SQLAlchemy модели
│   ├── schemas/             # Pydantic схемы
│   ├── api/                 # API роуты
│   └── services/            # Бизнес-логика
├── requirements.txt
└── README.md
```

