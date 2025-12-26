@echo off
chcp 65001 > nul
title VoxPersonal v6 - Умный помощник

echo.
echo ====================================================
echo            🤖 VoxPersonal v6
echo        Умный голосовой помощник
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

echo [2] Установка необходимых библиотек...
echo.

REM Установка основных библиотек
pip install --upgrade pip --quiet 2>nul

echo Устанавливаю SpeechRecognition...
pip install speechrecognition --quiet 2>nul

echo Устанавливаю pyttsx3...
pip install pyttsx3 --quiet 2>nul

echo Устанавливаю pyautogui...
pip install pyautogui --quiet 2>nul

echo Устанавливаю requests...
pip install requests --quiet 2>nul

echo Устанавливаю Pillow для графики...
pip install Pillow --quiet 2>nul

echo.
echo [3] Проверка установки...
python -c "import speech_recognition" 2>nul && echo ✅ SpeechRecognition установлен
python -c "import pyttsx3" 2>nul && echo ✅ pyttsx3 установлен
python -c "import pyautogui" 2>nul && echo ✅ pyautogui установлен
python -c "from PIL import Image" 2>nul && echo ✅ Pillow установлен

echo.
echo [4] Запуск помощника...
echo.
echo 🆕 НОВИНКА v6:
echo    • 🖥️  Графический интерфейс
echo    • 📱 Боковое меню с разделами
echo    • 👤 Управление аккаунтом
echo    • ⚙️ Расширенные настройки
echo.
echo 💡 Советы:
echo    • Выберите режим GUI для удобства
echo    • В GUI: нажмите 'Запустить помощника'
echo    • Говорите 'вокс' для активации
echo.

timeout /t 3 /nobreak >nul

python run.py

if errorlevel 1 (
    echo.
    echo ❌ Произошла ошибка
    echo.
    echo Попробуйте:
    echo 1. Запустить от администратора
    echo 2. Установить Tkinter:
    echo    Windows: Установите Python с 'tcl/tk and IDLE'
    echo    Linux: sudo apt-get install python3-tk
    echo    Mac: brew install python-tk
    echo 3. Проверить микрофон
    pause
)

exit /b 0