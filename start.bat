@echo off
chcp 65001 > nul
title VoxPersonal v5 - Умный помощник

echo.
echo ====================================================
echo            🤖 VoxPersonal v5
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

echo.
echo [3] Проверка установки...
python -c "import speech_recognition" 2>nul && echo ✅ SpeechRecognition установлен
python -c "import pyttsx3" 2>nul && echo ✅ pyttsx3 установлен
python -c "import pyautogui" 2>nul && echo ✅ pyautogui установлен

echo.
echo [4] Запуск помощника...
echo.
echo 🆕 НОВИНКА v5:
echo    • Команда 'вокс' для активации
echo    • 'вокс [команда]' для быстрого выполнения
echo    • 'открой сайт [название]' для открытия сайтов
echo.
echo 💡 Советы:
echo    • Убедитесь что микрофон включен
echo    • Говорите четко и не торопитесь
echo    • Для активации скажите "вокс" или "привет"
echo.

timeout /t 2 /nobreak >nul

python run.py

if errorlevel 1 (
    echo.
    echo ❌ Произошла ошибка
    echo.
    echo Попробуйте:
    echo 1. Запустить от администратора
    echo 2. pip install pyaudio
    echo 3. Проверить микрофон
    pause
)

exit /b 0