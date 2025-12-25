"""
VoxPersonal Super Lite v2 - Улучшенное распознавание речи
Команды: привет, как дела, открой браузер, открой панель управления, 
         громче, тише, пока
"""

import speech_recognition as sr
import pyttsx3
import json
import os
import webbrowser
import subprocess
from datetime import datetime
import time
import pyautogui

class SuperLiteAssistantV2:
    def __init__(self):
        self.name = "VoxPersonal v2"
        self.is_listening = False
        self.media_volume = 50  # Текущая громкость (0-100)
        
        # Улучшенная инициализация речи
        self.recognizer = sr.Recognizer()
        self.microphone = self._get_microphone()
        self.tts_engine = self._init_tts()
        
        # Настройка для лучшего распознавания
        self._setup_speech_recognition()
        
        # Команды (7 штук)
        self.commands = {
            "привет": self._hello,
            "как дела": self._how_are_you,
            "открой браузер": self._open_browser,
            "открой панель управления": self._open_control_panel,
            "громче": self._volume_up,
            "тише": self._volume_down,
            "пока": self._goodbye
        }
        
        print(f"🎙️ {self.name} запущен!")
        print("Доступные команды:")
        for cmd in self.commands.keys():
            print(f"  • {cmd}")
    
    def _get_microphone(self):
        """Получение микрофона с обработкой ошибок"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if mic_list:
                print(f"Доступные микрофоны: {mic_list}")
                return sr.Microphone()
            else:
                print("⚠️  Микрофоны не найдены, используется системный")
                return sr.Microphone()
        except Exception as e:
            print(f"⚠️  Ошибка микрофона: {e}")
            return sr.Microphone()
    
    def _setup_speech_recognition(self):
        """Настройка для лучшего распознавания"""
        try:
            with self.microphone as source:
                # Более длительная калибровка фонового шума
                print("🔧 Калибровка микрофона...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                # Более высокий порог для русского языка
                self.recognizer.energy_threshold = 400
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.dynamic_energy_adjustment_damping = 0.15
                self.recognizer.dynamic_energy_ratio = 1.5
                
                print("✅ Микрофон настроен")
        except Exception as e:
            print(f"⚠️  Ошибка настройки: {e}")
    
    def _init_tts(self):
        """Инициализация синтеза речи"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)  # Немного медленнее для ясности
        engine.setProperty('volume', 0.9)
        
        # Поиск русского голоса
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"✅ Используется голос: {voice.name}")
                break
        
        return engine
    
    def speak(self, text, wait=True):
        """Произнести текст"""
        print(f"[Ассистент]: {text}")
        self.tts_engine.say(text)
        if wait:
            self.tts_engine.runAndWait()
    
    def listen(self, timeout=5, phrase_time_limit=6):
        """
        Улучшенное прослушивание с лучшим распознаванием
        
        Returns:
            Текст или None
        """
        if not self.microphone:
            print("❌ Микрофон не доступен")
            return None
        
        with self.microphone as source:
            print("🎤 Слушаю... (скажите команду)")
            
            try:
                # Более чувствительные настройки для русского
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔍 Распознаю...")
                
                # Пробуем несколько сервисов для надежности
                try:
                    # Основной - Google (лучше всего для русского)
                    text = self.recognizer.recognize_google(
                        audio, 
                        language="ru-RU",
                        show_all=False
                    )
                    
                    if text:
                        print(f"[Вы сказали]: {text}")
                        return text.lower()
                    
                except sr.UnknownValueError:
                    # Пробуем другую конфигурацию
                    try:
                        text = self.recognizer.recognize_google(
                            audio, 
                            language="ru-RU",
                            show_all=False
                        )
                        if text:
                            print(f"[Вы сказали]: {text}")
                            return text.lower()
                    except:
                        pass
                
                print("❌ Не удалось распознать речь")
                return None
                
            except sr.WaitTimeoutError:
                print("⏰ Время ожидания истекло")
                return None
            except Exception as e:
                print(f"❌ Ошибка прослушивания: {e}")
                return None
    
    def listen_with_retry(self, max_attempts=3):
        """Прослушивание с повторными попытками"""
        for attempt in range(max_attempts):
            text = self.listen()
            if text:
                return text
            
            if attempt < max_attempts - 1:
                self.speak("Повторите, пожалуйста", wait=False)
                time.sleep(0.5)
        
        return None
    
    # Команды (7 штук)
    def _hello(self):
        """Команда: привет"""
        return "Привет! Я голосовой ассистент. Скажите 'открой браузер', 'громче' или 'тише'"
    
    def _how_are_you(self):
        """Команда: как дела"""
        return "Всё отлично! Готов помогать вам."
    
    def _open_browser(self):
        """Команда: открой браузер"""
        try:
            webbrowser.open("https://google.com")
            return "Открываю браузер с Google"
        except Exception as e:
            return f"Не удалось открыть браузер: {e}"
    
    def _open_control_panel(self):
        """Команда: открой панель управления"""
        try:
            # Для разных версий Windows
            if os.name == 'nt':
                subprocess.Popen(['control.exe'])
                return "Открываю панель управления"
            else:
                return "Эта команда работает только на Windows"
        except Exception as e:
            return f"Не удалось открыть панель управления: {e}"
    
    def _volume_up(self):
        """Команда: громче"""
        try:
            # Системная регулировка громкости
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            self.media_volume = min(100, self.media_volume + 20)
            return f"Громкость увеличена. Сейчас {self.media_volume}%"
        except Exception as e:
            return f"Не удалось увеличить громкость: {e}"
    
    def _volume_down(self):
        """Команда: тише"""
        try:
            # Системная регулировка громкости
            pyautogui.press('volumedown')
            pyautogui.press('volumedown')
            self.media_volume = max(0, self.media_volume - 20)
            return f"Громкость уменьшена. Сейчас {self.media_volume}%"
        except Exception as e:
            return f"Не удалось уменьшить громкость: {e}"
    
    def _goodbye(self):
        """Команда: пока"""
        self.is_listening = False
        return "Пока! Буду ждать вашего возвращения."
    
    def process_command(self, text):
        """Улучшенная обработка команды с частичным совпадением"""
        if not text:
            return False
        
        # Приводим к нижнему регистру и убираем лишние пробелы
        text = text.lower().strip()
        
        # Ищем команду (частичное совпадение)
        for cmd, func in self.commands.items():
            # Простое совпадение
            if cmd in text:
                result = func()
                self.speak(result)
                
                # Если команда "пока", останавливаемся
                if cmd == "пока":
                    return "stop"
                return True
            
            # Совпадение по словам (для коротких команд)
            cmd_words = cmd.split()
            text_words = text.split()
            
            if len(cmd_words) == 1 and len(text_words) == 1:
                # Для однословных команд проверяем похожесть
                if cmd_words[0] in text_words[0] or text_words[0] in cmd_words[0]:
                    result = func()
                    self.speak(result)
                    if cmd == "пока":
                        return "stop"
                    return True
        
        # Если команда не найдена, предлагаем помощь
        suggestions = []
        for cmd in self.commands.keys():
            if any(word in text for word in cmd.split()):
                suggestions.append(cmd)
        
        if suggestions:
            self.speak(f"Возможно, вы имели в виду: {', '.join(suggestions[:2])}")
        else:
            self.speak("Не понял. Скажите 'привет' для списка команд")
        
        return False
    
    def run(self):
        """Основной цикл с улучшенной логикой"""
        self.speak("Ассистент запущен. Скажите 'привет' для начала.")
        
        activation_count = 0
        
        while True:
            try:
                # Ждем команду активации (можно сказать просто "привет")
                print("\n🔍 Ожидание активации...")
                text = self.listen_with_retry(max_attempts=2)
                
                if text and ("привет" in text or "эй" in text or "окей" in text):
                    activation_count += 1
                    
                    if activation_count == 1:
                        self.speak("Да, слушаю вас! Доступные команды: открой браузер, громче, тише")
                    else:
                        self.speak("Да, что нужно?")
                    
                    # Основной режим прослушивания команд
                    command_count = 0
                    while True:
                        print(f"\n📝 Ожидание команды #{command_count + 1}...")
                        command = self.listen_with_retry(max_attempts=2)
                        
                        if command:
                            command_count += 1
                            result = self.process_command(command)
                            
                            if result == "stop":
                                print("👋 Завершение работы по команде 'пока'")
                                return
                            
                            # После 3 команд делаем паузу
                            if command_count >= 3:
                                self.speak("Сделаем паузу. Скажите 'привет' когда понадоблюсь.")
                                break
                        else:
                            # Если ничего не сказали, ждем еще немного
                            time.sleep(1)
                            
                elif text:
                    # Если сказали что-то другое, пробуем обработать
                    self.process_command(text)
                    
            except KeyboardInterrupt:
                self.speak("Завершение работы")
                break
            except Exception as e:
                print(f"❌ Ошибка в основном цикле: {e}")
                time.sleep(2)

# Простая функция для запуска
if __name__ == "__main__":
    print("=" * 50)
    print("VoxPersonal Super Lite v2 - Запуск")
    print("=" * 50)
    
    assistant = SuperLiteAssistantV2()
    assistant.run()