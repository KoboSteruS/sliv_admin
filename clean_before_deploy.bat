@echo off
echo ========================================
echo Очистка кэша перед деплоем
echo ========================================
echo.

REM Удаляем node_modules (используем PowerShell для более быстрого удаления)
if exist "wild-camels-nail\node_modules" (
    echo Удаление node_modules (это может занять несколько минут)...
    powershell -Command "Remove-Item -Path 'wild-camels-nail\node_modules' -Recurse -Force -ErrorAction SilentlyContinue"
    if exist "wild-camels-nail\node_modules" (
        echo ⚠ node_modules всё ещё существует, пробуем стандартный метод...
        timeout /t 2 /nobreak >nul
        rmdir /s /q "wild-camels-nail\node_modules" 2>nul
    )
    if not exist "wild-camels-nail\node_modules" (
        echo ✓ node_modules удалён
    ) else (
        echo ⚠ Не удалось удалить node_modules полностью, попробуйте удалить вручную
    )
) else (
    echo node_modules не найден
)

REM Удаляем venv (виртуальное окружение Python)
if exist "back\venv" (
    echo Удаление venv...
    powershell -Command "Remove-Item -Path 'back\venv' -Recurse -Force -ErrorAction SilentlyContinue"
    if not exist "back\venv" (
        echo ✓ venv удалён
    ) else (
        echo ⚠ venv всё ещё существует
    )
) else (
    echo venv не найден
)

REM Удаляем __pycache__ папки
echo Удаление __pycache__...
for /d /r "back" %%d in (__pycache__) do @if exist "%%d" (
    rmdir /s /q "%%d"
)
echo ✓ __pycache__ удалён

REM Удаляем .pyc файлы
echo Удаление .pyc файлов...
for /r "back" %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
echo ✓ .pyc файлы удалены

REM Удаляем кэш Vite
if exist "wild-camels-nail\.vite" (
    echo Удаление .vite...
    rmdir /s /q "wild-camels-nail\.vite"
    echo ✓ .vite удалён
)

REM Удаляем dist/build папки
if exist "wild-camels-nail\dist" (
    echo Удаление dist...
    rmdir /s /q "wild-camels-nail\dist"
    echo ✓ dist удалён
)
if exist "wild-camels-nail\build" (
    echo Удаление build...
    rmdir /s /q "wild-camels-nail\build"
    echo ✓ build удалён
)

REM Удаляем .next (если есть)
if exist "wild-camels-nail\.next" (
    echo Удаление .next...
    rmdir /s /q "wild-camels-nail\.next"
    echo ✓ .next удалён
)

REM Удаляем логи (опционально)
if exist "back\logs" (
    echo Удаление логов...
    del /q "back\logs\*.*" 2>nul
    echo ✓ Логи очищены
)

echo.
echo ========================================
echo ✓ Очистка завершена!
echo ========================================
echo.
echo Теперь можно копировать проект на сервер:
echo scp -r Sliv_Admin root@10.10.10.31:/root/
echo.
pause

