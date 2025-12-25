"""
Запуск VoxPersonal Super Lite v2
"""

import sys
import threading
import time
import os

def main():
    print("""
    ╔══════════════════════════════════════╗
    ║      🎙️ VoxPersonal v2             ║
    ║    Улучшенное распознавание речи     ║
    ╚══════════════════════════════════════╝
    """)
    
    print("🔍 Проверка системы...")
    
    # Проверяем Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Требуется Python 3.7 или выше")
        return
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Проверяем зависимости
    print("📦 Проверка зависимостей...")
    dependencies = [
        ('speech_recognition', 'speechrecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('flask', 'flask'),
        ('pyautogui', 'pyautogui'),
        ('requests', 'requests'),
        ('pyaudio', 'pyaudio')
    ]
    
    missing = []
    for import_name, pip_name in dependencies:
        try:
            __import__(import_name)
            print(f"  ✅ {pip_name}")
        except ImportError:
            print(f"  ❌ {pip_name}")
            missing.append(pip_name)
    
    if missing:
        print(f"\n⚠️  Отсутствуют библиотеки: {', '.join(missing)}")
        print("   Установите: pip install " + " ".join(missing))
        
        install_now = input("   Установить сейчас? (y/n): ").lower()
        if install_now == 'y':
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Библиотеки установлены!")
        else:
            print("❌ Установите зависимости перед запуском")
            return
    
    # Проверяем микрофон
    print("\n🎤 Проверка микрофона...")
    try:
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        if mics:
            print(f"✅ Найдено микрофонов: {len(mics)}")
            print(f"   Используется: {mics[0]}")
        else:
            print("⚠️  Микрофоны не найдены, но попробуем продолжить")
    except Exception as e:
        print(f"⚠️  Ошибка проверки микрофона: {e}")
    
    # Создаем папки если нужно
    print("\n📁 Создание структуры...")
    os.makedirs("shared", exist_ok=True)
    
    # Сохраняем команды если файла нет
    commands_file = "shared/commands.json"
    if not os.path.exists(commands_file):
        import json
        commands = {
            "привет": {"response": "Привет! Я голосовой ассистент", "type": "basic"},
            "как дела": {"response": "Всё отлично!", "type": "basic"},
            "открой браузер": {"action": "open_browser", "type": "system"},
            "открой панель управления": {"action": "open_control_panel", "type": "system"},
            "громче": {"action": "volume_up", "type": "media"},
            "тише": {"action": "volume_down", "type": "media"},
            "пока": {"response": "До свидания!", "type": "control"}
        }
        with open(commands_file, 'w', encoding='utf-8') as f:
            json.dump(commands, f, ensure_ascii=False, indent=2)
        print("✅ Файл команд создан")
    
    # Запускаем веб-панель
    print("\n🌐 Запуск веб-панели...")
    from web_panel import run_web_server
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    time.sleep(1)  # Даем время веб-серверу запуститься
    
    print("\n" + "="*60)
    print("🎉 Система готова к работе!")
    print("="*60)
    print("\n📢 ДОСТУПНЫЕ КОМАНДЫ:")
    print("   1. 🗣️  'привет' - Активация")
    print("   2. 😊 'как дела' - Спросить как дела")
    print("   3. 🌐 'открой браузер' - Открыть Google")
    print("   4. ⚙️  'открой панель управления' - Панель управления Windows")
    print("   5. 🔊 'громче' - Увеличить громкость")
    print("   6. 🔉 'тише' - Уменьшить громкость")
    print("   7. 👋 'пока' - Завершить работу")
    print("\n🌐 ВЕБ-ПАНЕЛЬ: http://localhost:5000")
    print("\n💡 СОВЕТЫ:")
    print("   • Говорите четко и не слишком быстро")
    print("   • После 'привет' ждите ответа ассистента")
    print("   • Для выхода скажите 'пока' или нажмите Ctrl+C")
    print("="*60 + "\n")
    
    # Запускаем ассистента
    print("🎙️ Запуск голосового ассистента...\n")
    
    from assistant import SuperLiteAssistantV2
    assistant = SuperLiteAssistantV2()
    
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 Завершение работы по запросу пользователя")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("   Перезапустите программу")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Выход")
        sys.exit(0)