"""
Запуск VoxPersonal v6 - выбор режима работы
"""

import sys
import os
import subprocess

def check_dependencies():
    """Проверка минимальных зависимостей"""
    print("🔍 Проверка библиотек...")
    
    libs = [
        ('speech_recognition', 'speechrecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pyautogui', 'pyautogui'),
        ('PIL', 'Pillow'),
        ('tkinter', 'tkinter')
    ]
    
    missing = []
    for import_name, pip_name in libs:
        try:
            if import_name == 'speech_recognition':
                import speech_recognition
            elif import_name == 'tkinter':
                import tkinter
            else:
                __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name}")
            missing.append(pip_name)
    
    if missing:
        if 'tkinter' in missing:
            print("\n❌ Tkinter не установлен!")
            print("Для Windows: Установите Python с опцией 'tcl/tk and IDLE'")
            print("Для Linux: sudo apt-get install python3-tk")
            print("Для Mac: brew install python-tk")
        else:
            print(f"\n📦 Установите: pip install " + " ".join([m for m in missing if m != 'tkinter']))
        return False
    
    return True

def main():
    print("""
    ╔══════════════════════════════════════════╗
    ║        🤖 VoxPersonal v6                ║
    ║      Умный голосовой помощник           ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Проверка Python
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7+")
        return
    
    # Проверка зависимостей
    if not check_dependencies():
        print("\n❌ Установите зависимости и перезапустите")
        return
    
    print("\n" + "="*60)
    print("🎉 Система готова к работе!")
    print("="*60)
    
    print("\n🚀 Выберите режим работы:")
    print("   1. 📱 Графический интерфейс (GUI)")
    print("   2. 🖥️  Командная строка (CLI)")
    print("   3. ❌ Выход")
    print("="*60)
    
    while True:
        choice = input("\nВаш выбор (1-3): ").strip()
        
        if choice == '1':
            print("\n🚀 Запуск графического интерфейса...")
            try:
                from gui_app import main as gui_main
                gui_main()
            except ImportError as e:
                print(f"❌ Ошибка: {e}")
                print("Убедитесь, что файл gui_app.py существует")
            break
            
        elif choice == '2':
            print("\n🚀 Запуск в режиме командной строки...")
            try:
                from assistant import VoxPersonalV6
                assistant = VoxPersonalV6()
                assistant.run()
            except ImportError:
                print("❌ Файл assistant.py не найден!")
            break
            
        elif choice == '3':
            print("\n👋 До свидания!")
            break
            
        else:
            print("❌ Неверный выбор. Введите 1, 2 или 3")

if __name__ == "__main__":
    main()