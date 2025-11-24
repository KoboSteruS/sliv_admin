@echo off
echo ========================================
echo Быстрая очистка кэша (PowerShell)
echo ========================================
echo.

echo Удаление node_modules, venv и кэша...
powershell -Command ^
    "$ErrorActionPreference='SilentlyContinue'; ^
    Remove-Item -Path 'wild-camels-nail\node_modules' -Recurse -Force; ^
    Remove-Item -Path 'back\venv' -Recurse -Force; ^
    Get-ChildItem -Path 'back' -Recurse -Filter '__pycache__' -Directory | Remove-Item -Recurse -Force; ^
    Get-ChildItem -Path 'back' -Recurse -Filter '*.pyc' -File | Remove-Item -Force; ^
    Remove-Item -Path 'wild-camels-nail\.vite' -Recurse -Force; ^
    Remove-Item -Path 'wild-camels-nail\dist' -Recurse -Force; ^
    Remove-Item -Path 'wild-camels-nail\build' -Recurse -Force; ^
    Write-Host '✓ Очистка завершена'"

echo.
echo ========================================
echo ✓ Готово к копированию!
echo ========================================
echo.
pause

