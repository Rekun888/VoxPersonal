"""
Запуск VoxPersonal v3
"""

import sys
import threading
import time
import os
import json

def main():
    print("""
    ╔══════════════════════════════════════╗
    ║      🎙️ VoxPersonal v3             ║
    ║    Управление медиа • 10 команд      ║
    ╚══════════════════════════════════════╝
    """)
    
    print("🔍 Проверка системы...")
    
    # Проверяем Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Требуется Python 3.7+")
        return
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Проверяем зависимости
    print("\n📦 Проверка зависимостей...")
    deps = [
        ('speech_recognition', 'speechrecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pyautogui', 'pyautogui'),
        ('psutil', 'psutil')
    ]
    
    missing = []
    for import_name, pip_name in deps:
        try:
            __import__(import_name)
            print(f"  ✅ {pip_name}")
        except ImportError:
            print(f"  ❌ {pip_name}")
            missing.append(pip_name)
    
    if missing:
        print(f"\n⚠️  Установка: pip install " + " ".join(missing))
        
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Библиотеки установлены!")
            # Перезапускаем после установки
            print("🔄 Перезапуск...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except:
            print("❌ Ошибка установки")
            print("Установите вручную: pip install " + " ".join(missing))
            return
    
    # Создаем структуру
    print("\n📁 Создание структуры...")
    os.makedirs("shared", exist_ok=True)
    
    # Сохраняем команды
    commands_file = "shared/commands.json"
    if not os.path.exists(commands_file):
        commands = {
            "привет": {"response": "Привет! Рад вас слышать", "type": "basic"},
            "как дела": {"response": "Всё прекрасно!", "type": "basic"},
            "открой браузер": {"action": "open_browser", "type": "system"},
            "закрой браузер": {"action": "close_browser", "type": "system"},
            "открой панель управления": {"action": "open_control_panel", "type": "system"},
            "громче": {"action": "volume_up", "type": "media"},
            "тише": {"action": "volume_down", "type": "media"},
            "стоп": {"action": "media_stop", "type": "media"},
            "пауза": {"action": "media_pause_play", "type": "media"},
            "продолжи": {"action": "media_pause_play", "type": "media"},
            "пока": {"response": "До свидания!", "type": "control"}
        }
        with open(commands_file, 'w', encoding='utf-8') as f:
            json.dump(commands, f, ensure_ascii=False, indent=2)
        print("✅ Файл команд создан")
    
    # Проверяем наличие веб-панели, но не запускаем её автоматически
    try:
        import web_panel
        print("✅ Веб-панель доступна")
        # Запускаем веб-панель в отдельном потоке
        print("\n🌐 Запуск веб-панели...")
        web_thread = threading.Thread(target=web_panel.run_web_server, daemon=True)
        web_thread.start()
        time.sleep(1)
        print("🌐 Веб-панель: http://localhost:5000")
    except ImportError:
        print("⚠️  Веб-панель не найдена, продолжаем без неё")
    
    print("\n" + "="*60)
    print("🎉 VoxPersonal v3 готов к работе!")
    print("="*60)
    
    print("\n📢 ОСНОВНЫЕ КОМАНДЫ:")
    print("   1. 🗣️  'привет' - Приветствие")
    print("   2. 😊 'как дела' - Спросить как дела")
    print("   3. 🌐 'открой браузер' - Открыть Google")
    print("   4. ❌ 'закрой браузер' - Закрыть браузер")
    print("   5. ⚙️  'открой панель управления' - Панель управления")
    
    print("\n🎵 УПРАВЛЕНИЕ МЕДИА:")
    print("   6. 🔊 'громче' - Увеличить громкость")
    print("   7. 🔉 'тише' - Уменьшить громкость")
    print("   8. ⏹️  'стоп' - Остановить воспроизведение")
    print("   9. ⏸️  'пауза' - Пауза/продолжить")
    print("   10. ▶️  'продолжи' - Продолжить воспроизведение")
    print("   11. 👋 'пока' - Завершить работу")
    
    print("\n⌨️  ГОРЯЧИЕ КЛАВИШИ:")
    print("   • Пробел - Пауза/продолжить")
    print("   • Esc - Стоп")
    print("   • F2 - Привет")
    
    print("\n💡 СОВЕТЫ:")
    print("   • Говорите чётко и не торопитесь")
    print("   • После команды ждите ответа ассистента")
    print("   • Для лучшего распознавания используйте полные фразы")
    print("="*60 + "\n")
    
    # Запускаем ассистента
    print("🎙️ Запуск голосового ассистента...\n")
    
    try:
        from assistant import VoxPersonalV3
        assistant = VoxPersonalV3()
        
        try:
            assistant.run()
        except KeyboardInterrupt:
            print("\n\n👋 Завершение работы")
        except Exception as e:
            print(f"\n❌ Ошибка в работе ассистента: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"\n❌ Не удалось импортировать ассистента: {e}")
        print("Проверьте наличие файла assistant.py")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()