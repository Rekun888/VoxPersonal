@echo off
chcp 65001 > nul
title VOX PERSONAL v6 - PREMIUM LAUNCHER
mode con: cols=70 lines=25

:: Очистка экрана
cls

:: Современный баннер
echo.
echo      ╔══════════════════════════════════════════╗
echo      ║                                         ║
echo      ║        ██╗   ██╗ ██████╗ ██╗  ██╗       ║
echo      ║        ██║   ██║██╔═══██╗╚██╗██╔╝       ║
echo      ║        ██║   ██║██║   ██║ ╚███╔╝        ║
echo      ║        ╚██╗ ██╔╝██║   ██║ ██╔██╗        ║
echo      ║         ╚████╔╝ ╚██████╔╝██╔╝ ██╗       ║
echo      ║          ╚═══╝   ╚═════╝ ╚═╝  ╚═╝       ║
echo      ║                                         ║
echo      ║          V O X   P E R S O N A L        ║
echo      ║                 v6.0                    ║
echo      ╚══════════════════════════════════════════╝
echo.

:: Проверка системы
echo [SYSTEM CHECK]
echo.

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ CRITICAL: Python not found
    echo    Download from: https://python.org
    echo.
    pause
    exit /b 1
)

echo    ✅ Python OK

:: Проверка Tkinter
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo    ❌ ERROR: Tkinter missing
    echo.
    echo    Windows: Reinstall Python with 'tcl/tk' option
    echo    Linux:   sudo apt-get install python3-tk
    echo    Mac:     brew install python-tk
    echo.
    pause
    exit /b 1
)

echo    ✅ Tkinter OK

:: Запуск приложения
echo.
echo [LAUNCHING]
echo.
echo    ⚡ Initializing premium interface...
echo    🎨 Loading modern design...
echo    🔥 Starting VOX PERSONAL v6...
echo.

:: Краткая задержка с анимацией
for /l %%i in (1,1,3) do (
    echo    Starting.%%i
    timeout /t 1 /nobreak >nul
)

cls

:: Запуск Python приложения
echo.
echo    🚀 VOX PERSONAL v6 - PREMIUM INTERFACE
echo    ═══════════════════════════════════════════
echo.
echo    Features:
echo    • Ultra-modern dark theme
echo    • Neon color scheme
echo    • Smooth animations
echo    • Glassmorphism effects
echo    • Premium UI/UX
echo.
timeout /t 2 /nobreak >nul

:: Основной запуск
python app.py

:: Обработка ошибок
if errorlevel 1 (
    echo.
    echo    ⚠️  LAUNCH FAILED
    echo    ═══════════════════════════════════════════
    echo.
    echo    Possible solutions:
    echo    1. Check app.py exists in current folder
    echo    2. Run as Administrator
    echo    3. Ensure Tkinter is properly installed
    echo.
    pause
) else (
    echo.
    echo    ✅ Application closed successfully
    timeout /t 2 /nobreak >nul
)

exit