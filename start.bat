@echo off
chcp 65001 > nul
title VoxPersonal v2 - Улучшенное распознавание

echo.
echo ====================================================
echo         🎙️ VoxPersonal v2
echo    Улучшенное распознавание речи • 7 команд
echo ====================================================
echo.

echo [1] Проверка Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен или не найден!
    echo.
    echo Скачайте Python 3.7+ с официального сайта:
    echo https://www.python.org/downloads/
    echo.
    echo После установки перезапустите командную строку
    echo.
    pause
    exit /b 1
)

echo [2] Проверка и установка библиотек...
echo.
python -c "import speech_recognition" 2>nul
if errorlevel 1 (
    echo 📦 Установка speechrecognition...
    pip install speechrecognition --quiet
)

python -c "import pyttsx3" 2>nul
if errorlevel 1 (
    echo 📦 Установка pyttsx3...
    pip install pyttsx3 --quiet
)

python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 Установка flask...
    pip install flask --quiet
)

python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo 📦 Установка pyautogui...
    pip install pyautogui --quiet
)

python -c "import requests" 2>nul
if errorlevel 1 (
    echo 📦 Установка requests...
    pip install requests --quiet
)

python -c "import pyaudio" 2>nul
if errorlevel 1 (
    echo 📦 Установка pyaudio...
    echo Если возникает ошибка, скачайте .whl файл:
    echo https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    pip install pyaudio --quiet 2>nul || echo ⚠️ Pyaudio может потребовать ручной установки
)

echo.
echo [3] Создание папок...
if not exist "shared" mkdir shared

echo.
echo [4] Запуск системы...
echo.
echo 📢 ДОСТУПНЫЕ КОМАНДЫ:
echo   1. привет
echo   2. как дела
echo   3. открой браузер
echo   4. открой панель управления
echo   5. громче
echo   6. тише
echo   7. пока
echo.
echo 🌐 Веб-панель: http://localhost:5000
echo.
echo 💡 Говорите четко и ждите ответа ассистента
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ❌ Произошла ошибка при запуске
    echo.
    echo 🔧 Решение проблем:
    echo   1. Проверьте подключение к интернету
    echo   2. Убедитесь что микрофон подключен
    echo   3. Попробуйте запустить от имени администратора
    echo.
    pause
)

exit /b 0