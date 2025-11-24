@echo off
echo ========================================
echo Запуск Sliv Admin Backend
echo ========================================
echo.

REM Активируем виртуальное окружение
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Виртуальное окружение активировано
) else (
    echo ОШИБКА: Виртуальное окружение не найдено!
    echo Создайте его командой: python -m venv venv
    pause
    exit /b 1
)

echo.
echo Проверка зависимостей...
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo Установка зависимостей...
    pip install -r requirements.txt
)

echo.
echo Запуск сервера на http://localhost:8100
echo Для остановки нажмите Ctrl+C
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8100

pause

