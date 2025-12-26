"""
VoxPersonal v3 - Ассистент с управлением медиа
Команды: привет, как дела, открой браузер, закрой браузер,
         открой панель управления, громче, тише, стоп, пауза, пока
"""

import speech_recognition as sr
import pyttsx3
import json
import os
import webbrowser
import subprocess
import time
import pyautogui
import psutil

class VoxPersonalV3:
    def __init__(self):
        self.name = "VoxPersonal v3"
        self.is_listening = False
        self.media_volume = 50
        self.media_state = "stopped"  # stopped, playing, paused
        
        # Инициализация речи
        self.recognizer = sr.Recognizer()
        self.microphone = self._get_microphone()
        self.tts_engine = self._init_tts()
        
        # Настройка распознавания
        self._setup_speech_recognition()
        
        # Команды (9 штук)
        self.commands = {
            "привет": self._hello,
            "как дела": self._how_are_you,
            "открой браузер": self._open_browser,
            "закрой браузер": self._close_browser,
            "открой панель управления": self._open_control_panel,
            "громче": self._volume_up,
            "тише": self._volume_down,
            "стоп": self._media_stop,
            "пауза": self._media_pause_play,
            "продолжи": self._media_pause_play,
            "пока": self._goodbye
        }
        
        print(f"🎙️ {self.name} запущен!")
        print("Доступные команды:")
        commands_list = [
            "привет", "как дела", "открой браузер", "закрой браузер",
            "открой панель управления", "громче", "тише", "стоп", 
            "пауза/продолжи", "пока"
        ]
        for cmd in commands_list:
            print(f"  • {cmd}")
    
    def _get_microphone(self):
        """Получение микрофона"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if mic_list:
                print(f"✅ Найден микрофон: {mic_list[0]}")
                return sr.Microphone(device_index=0)
            else:
                print("⚠️  Используется системный микрофон")
                return sr.Microphone()
        except Exception as e:
            print(f"⚠️  Ошибка микрофона: {e}")
            return sr.Microphone()
    
    def _setup_speech_recognition(self):
        """Настройка распознавания"""
        try:
            with self.microphone as source:
                print("🔧 Калибровка микрофона...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                self.recognizer.energy_threshold = 350
                self.recognizer.dynamic_energy_threshold = True
                print("✅ Микрофон настроен")
        except Exception as e:
            print(f"⚠️  Ошибка настройки: {e}")
    
    def _init_tts(self):
        """Инициализация синтеза речи"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 0.9)
        
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
    
    def listen(self, timeout=4, phrase_time_limit=5):
        """Слушать микрофон"""
        with self.microphone as source:
            print("🎤 Слушаю...")
            
            try:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔍 Распознаю...")
                text = self.recognizer.recognize_google(audio, language="ru-RU")
                
                if text:
                    print(f"[Вы]: {text}")
                    return text.lower()
                
                return None
                
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                return None
    
    # Команды (9 основных)
    def _hello(self):
        """Команда: привет - только приветствие"""
        return "Привет! Рад вас слышать. Чем могу помочь?"
    
    def _how_are_you(self):
        """Команда: как дела"""
        return "Всё прекрасно! Готов выполнять ваши команды."
    
    def _open_browser(self):
        """Команда: открой браузер"""
        try:
            webbrowser.open("https://google.com")
            return "Браузер открыт с Google"
        except Exception as e:
            return f"Не удалось открыть браузер: {e}"
    
    def _close_browser(self):
        """Команда: закрой браузер"""
        try:
            # Закрываем основные браузеры
            browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe']
            closed = 0
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in browsers:
                        proc.kill()
                        closed += 1
                except:
                    continue
            
            if closed > 0:
                return f"Закрыто {closed} браузеров"
            else:
                return "Браузеры не найдены в запущенных процессах"
                
        except Exception as e:
            return f"Ошибка при закрытии браузера: {e}"
    
    def _open_control_panel(self):
        """Команда: открой панель управления"""
        try:
            if os.name == 'nt':
                os.system("control")
                return "Открываю панель управления Windows"
            else:
                return "Эта команда только для Windows"
        except Exception as e:
            return f"Не удалось открыть панель управления: {e}"
    
    def _volume_up(self):
        """Команда: громче"""
        try:
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            self.media_volume = min(100, self.media_volume + 20)
            return f"Громкость увеличена до {self.media_volume}%"
        except Exception as e:
            return f"Не удалось увеличить громкость: {e}"
    
    def _volume_down(self):
        """Команда: тише"""
        try:
            pyautogui.press('volumedown')
            pyautogui.press('volumedown')
            self.media_volume = max(0, self.media_volume - 20)
            return f"Громкость уменьшена до {self.media_volume}%"
        except Exception as e:
            return f"Не удалось уменьшить громкость: {e}"
    
    def _media_stop(self):
        """Команда: стоп - остановить медиа"""
        try:
            pyautogui.press('stop')
            self.media_state = "stopped"
            return "Воспроизведение остановлено"
        except Exception as e:
            return f"Не удалось остановить воспроизведение: {e}"
    
    def _media_pause_play(self):
        """Команда: пауза/продолжи - пауза или продолжение"""
        try:
            pyautogui.press('playpause')
            
            if self.media_state == "playing":
                self.media_state = "paused"
                return "Поставлено на паузу"
            else:
                self.media_state = "playing"
                return "Воспроизведение продолжено"
                
        except Exception as e:
            return f"Не удалось управлять воспроизведением: {e}"
    
    def _goodbye(self):
        """Команда: пока"""
        self.is_listening = False
        return "До свидания! Обращайтесь ещё."
    
    def process_command(self, text):
        """Обработка команды"""
        if not text:
            return False
        
        # Ищем точное или частичное совпадение
        for cmd, func in self.commands.items():
            if cmd in text:
                result = func()
                self.speak(result)
                
                if cmd == "пока":
                    return "stop"
                return True
        
        # Синонимы и альтернативные варианты
        synonyms = {
            "здравствуй": "привет",
            "добрый день": "привет",
            "выключи": "закрой",
            "останови": "стоп",
            "замолчи": "стоп",
            "включи": "пауза",
            "давай": "продолжи"
        }
        
        for synonym, command in synonyms.items():
            if synonym in text and command in self.commands:
                result = self.commands[command]()
                self.speak(result)
                
                if command == "пока":
                    return "stop"
                return True
        
        # Если команда не найдена
        self.speak("Извините, не понял команду. Попробуйте ещё раз.")
        return False
    
    def run(self):
        """Основной цикл работы"""
        self.speak(f"{self.name} запущен. Скажите 'привет' для начала.")
        
        while True:
            try:
                # Ждем активации
                print("\n🔍 Ожидание активации...")
                text = self.listen()
                
                if text and ("привет" in text or "эй" in text or "слушай" in text):
                    self.speak("Да, слушаю вас!")
                    
                    # Режим выполнения команд
                    while True:
                        print("\n📝 Ожидание команды...")
                        command = self.listen()
                        
                        if command:
                            result = self.process_command(command)
                            
                            if result == "stop":
                                print("👋 Завершение работы")
                                return
                            
                        else:
                            # Если тишина более 10 секунд, возвращаемся в режим ожидания
                            time.sleep(1)
                            
                elif text:
                    # Если сказали что-то без активации, пробуем обработать
                    self.process_command(text)
                    
            except KeyboardInterrupt:
                self.speak("Завершение работы")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                time.sleep(1)

if __name__ == "__main__":
    print("=" * 50)
    print("VoxPersonal v3 - Управление медиа")
    print("=" * 50)
    
    assistant = VoxPersonalV3()
    assistant.run()