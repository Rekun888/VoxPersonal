"""
Запуск VoxPersonal Super Lite
"""

import sys
import threading

def main():
    print("""
    ╔══════════════════════════════════════╗
    ║      🎙️ VoxPersonal Super Lite      ║
    ║        5 команд • 1 файл            ║
    ╚══════════════════════════════════════╝
    """)
    
    # Проверяем зависимости
    print("📦 Проверка зависимостей...")
    try:
        import speech_recognition
        import pyttsx3
        import flask
        import pyautogui
        print("✅ Все зависимости установлены")
    except ImportError as e:
        print(f"❌ Отсутствует библиотека: {e}")
        print("   Установите: pip install -r requirements.txt")
        return
    
    # Запускаем веб-панель в отдельном потоке
    print("🌐 Запуск веб-панели...")
    print("   Откройте: http://localhost:5000")
    
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Запускаем ассистента
    print("🎙️ Запуск голосового ассистента...")
    print("\n" + "="*50)
    print("Доступные команды:")
    print("  1. привет")
    print("  2. как дела")
    print("  3. открой браузер")
    print("  4. открой панель управления")
    print("  5. стоп")
    print("="*50 + "\n")
    
    from assistant import SuperLiteAssistant
    assistant = SuperLiteAssistant()
    assistant.run()

def run_web_server():
    """Запуск веб-сервера"""
    from web_panel import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Завершение работы...")
        sys.exit(0)