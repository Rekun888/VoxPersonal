@echo off
chcp 65001 > nul
title VoxPersonal v3

echo.
echo ====================================================
echo         🎙️ VoxPersonal v3
echo ====================================================
echo.

echo [1] Проверка Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo Скачайте с: https://python.org/downloads/
    pause
    exit /b 1
)

echo [2] Проверка и установка библиотек...
echo.

REM --- Проверяем базовые библиотеки ---
python -c "import speech_recognition" 2>nul
if errorlevel 1 (
    echo Устанавливаю speechrecognition...
    pip install speechrecognition --quiet
)

python -c "import pyttsx3" 2>nul
if errorlevel 1 (
    echo Устанавливаю pyttsx3...
    pip install pyttsx3 --quiet
)

python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo Устанавливаю pyautogui...
    pip install pyautogui --quiet
)

REM --- Пробуем установить psutil ---
echo Пробую установить psutil...
pip install psutil --quiet 2>nul
if errorlevel 1 (
    echo ❌ Не удалось установить psutil стандартным способом
    echo Пробую альтернативный способ...
    pip install psutil==5.9.5 --no-build-isolation --quiet 2>nul
    if errorlevel 1 (
        echo ❌ psutil не установлен, работаем без него
        echo Создаю заглушку для psutil...
        
        REM Создаем файл-заглушку psutil.py
        echo import sys > psutil_stub.py
        echo.
        echo class Process: >> psutil_stub.py
        echo    def __init__(self): >> psutil_stub.py
        echo        pass >> psutil_stub.py
        echo.
        echo def process_iter(attrs=None): >> psutil_stub.py
        echo    return [] >> psutil_stub.py
    )
)

echo.
echo [3] Создание папок...
if not exist "shared" mkdir shared

echo.
echo [4] Запуск системы...
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при запуске
    echo Попробуйте: pip install psutil
    pause
)

exit /b 0