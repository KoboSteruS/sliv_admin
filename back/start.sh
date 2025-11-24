#!/bin/bash

echo "========================================"
echo "Запуск Sliv Admin Backend"
echo "========================================"
echo ""

# Активируем виртуальное окружение
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Виртуальное окружение активировано"
else
    echo "ОШИБКА: Виртуальное окружение не найдено!"
    echo "Создайте его командой: python3 -m venv venv"
    exit 1
fi

echo ""
echo "Проверка зависимостей..."
python -c "import uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Установка зависимостей..."
    pip install -r requirements.txt
fi

echo ""
echo "Запуск сервера на http://localhost:8000"
echo "Для остановки нажмите Ctrl+C"
echo ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

