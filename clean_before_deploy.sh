#!/bin/bash

echo "========================================"
echo "Очистка кэша перед деплоем"
echo "========================================"
echo ""

# Удаляем node_modules
if [ -d "wild-camels-nail/node_modules" ]; then
    echo "Удаление node_modules..."
    rm -rf "wild-camels-nail/node_modules"
    echo "✓ node_modules удалён"
else
    echo "node_modules не найден"
fi

# Удаляем venv (виртуальное окружение Python)
if [ -d "back/venv" ]; then
    echo "Удаление venv..."
    rm -rf "back/venv"
    echo "✓ venv удалён"
else
    echo "venv не найден"
fi

# Удаляем __pycache__ папки
echo "Удаление __pycache__..."
find back -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✓ __pycache__ удалён"

# Удаляем .pyc файлы
echo "Удаление .pyc файлов..."
find back -type f -name "*.pyc" -delete 2>/dev/null
echo "✓ .pyc файлы удалены"

# Удаляем кэш Vite
if [ -d "wild-camels-nail/.vite" ]; then
    echo "Удаление .vite..."
    rm -rf "wild-camels-nail/.vite"
    echo "✓ .vite удалён"
fi

# Удаляем dist/build папки
if [ -d "wild-camels-nail/dist" ]; then
    echo "Удаление dist..."
    rm -rf "wild-camels-nail/dist"
    echo "✓ dist удалён"
fi

if [ -d "wild-camels-nail/build" ]; then
    echo "Удаление build..."
    rm -rf "wild-camels-nail/build"
    echo "✓ build удалён"
fi

# Удаляем .next (если есть)
if [ -d "wild-camels-nail/.next" ]; then
    echo "Удаление .next..."
    rm -rf "wild-camels-nail/.next"
    echo "✓ .next удалён"
fi

# Удаляем логи (опционально)
if [ -d "back/logs" ]; then
    echo "Удаление логов..."
    rm -f back/logs/*.log 2>/dev/null
    echo "✓ Логи очищены"
fi

echo ""
echo "========================================"
echo "✓ Очистка завершена!"
echo "========================================"
echo ""
echo "Теперь можно копировать проект на сервер:"
echo "scp -r Sliv_Admin root@10.10.10.31:/root/"
echo ""

