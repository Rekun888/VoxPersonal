"""
Запуск VoxPersonal v5
"""

import sys
import os

def check_dependencies():
    """Проверка минимальных зависимостей"""
    print("🔍 Проверка библиотек...")
    
    libs = [
        ('speech_recognition', 'speechrecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pyautogui', 'pyautogui')
    ]
    
    missing = []
    for import_name, pip_name in libs:
        try:
            if import_name == 'speech_recognition':
                import speech_recognition
            else:
                __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name}")
            missing.append(pip_name)
    
    if missing:
        print(f"\n📦 Установите: pip install " + " ".join(missing))
        return False
    
    return True

def main():
    print("""
    ╔══════════════════════════════════════════╗
    ║        🤖 VoxPersonal v5                ║
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
    
    print("\n🚀 Новые возможности v5:")
    print("   • 'вокс' - Новая команда активации")
    print("   • 'вокс [команда]' - Быстрая активация с командой")
    print("   • 'открой сайт [название]' - Открыть любой сайт")
    print("="*60)
    
    print("\n🚀 Популярные команды:")
    print("   • 'вокс' или 'привет' - Активировать помощника")
    print("   • 'открой сайт гитхаб' - Открыть GitHub")
    print("   • 'сколько времени' - Узнать время")
    print("   • 'расскажи шутку' - Развеселиться")
    print("   • 'сделай скриншот' - Сделать скрин")
    print("   • 'что ты умеешь' - Все команды")
    print("   • 'пока' - Завершить работу")
    print("="*60 + "\n")
    
    # Запуск
    try:
        from assistant import VoxPersonalV5
        assistant = VoxPersonalV5()
        assistant.run()
    except ImportError:
        print("❌ Файл assistant.py не найден!")
    except KeyboardInterrupt:
        print("\n👋 Завершение работы")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    main()