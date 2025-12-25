@echo off
chcp 65001 > nul
title VoxPersonal Super Lite

echo.
echo ========================================
echo     🎙️ VoxPersonal Super Lite
echo ========================================
echo.

echo [1] Проверка Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo Скачайте с: https://python.org
    pause
    exit /b 1
)

echo [2] Установка библиотек...
pip install speechrecognition pyttsx3 flask pyautogui requests --quiet

echo [3] Запуск системы...
echo.
echo 📢 Доступные команды:
echo   • привет
echo   • как дела
echo   • открой браузер
echo   • открой панель управления
echo   • стоп
echo.
echo 🌐 Веб-панель: http://localhost:5000
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ❌ Произошла ошибка
    pause
)

exit /b 0