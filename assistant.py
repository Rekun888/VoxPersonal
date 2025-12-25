"""
VoxPersonal Super Lite - Минимальный голосовой ассистент
Только 5 команд: привет, как дела, открой браузер, открой панель управления, стоп
"""

import speech_recognition as sr
import pyttsx3
import json
import os
import webbrowser
import subprocess
from datetime import datetime

class SuperLiteAssistant:
    def __init__(self):
        self.name = "VoxPersonal Super Lite"
        self.is_listening = False
        
        # Инициализация речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self._init_tts()
        
        # Базовые команды (всего 5!)
        self.commands = {
            "привет": self._hello,
            "как дела": self._how_are_you,
            "открой браузер": self._open_browser,
            "открой панель управления": self._open_control_panel,
            "стоп": self._stop
        }
        
        print(f"🎙️ {self.name} запущен!")
        print("Доступные команды:")
        for cmd in self.commands.keys():
            print(f"  • {cmd}")
    
    def _init_tts(self):
        """Инициализация синтеза речи"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)  # Скорость
        engine.setProperty('volume', 0.9)  # Громкость
        
        # Поиск русского голоса
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        return engine
    
    def speak(self, text):
        """Произнести текст"""
        print(f"[Ассистент]: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self, timeout=3):
        """Слушать микрофон"""
        with self.microphone as source:
            print("🎤 Слушаю...")
            self.recognizer.adjust_for_ambient_noise(source)
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language="ru-RU")
                print(f"[Вы]: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                print("Ошибка соединения")
                return None
    
    # Команды (всего 5!)
    def _hello(self):
        """Команда: привет"""
        return "Привет! Я голосовой ассистент. Скажите 'открой браузер' или 'открой панель управления'"
    
    def _how_are_you(self):
        """Команда: как дела"""
        return "Всё отлично! Готов помогать вам."
    
    def _open_browser(self):
        """Команда: открой браузер"""
        webbrowser.open("https://google.com")
        return "Открываю браузер с Google"
    
    def _open_control_panel(self):
        """Команда: открой панель управления"""
        try:
            # Для Windows
            os.system("control")
            return "Открываю панель управления"
        except:
            return "Не удалось открыть панель управления"
    
    def _stop(self):
        """Команда: стоп"""
        self.is_listening = False
        return "До свидания! Для запуска снова запустите программу."
    
    def process_command(self, text):
        """Обработка команды"""
        if not text:
            return False
        
        # Ищем команду
        for cmd, func in self.commands.items():
            if cmd in text:
                result = func()
                self.speak(result)
                
                # Если команда "стоп", останавливаемся
                if cmd == "стоп":
                    return "stop"
                return True
        
        # Если команда не найдена
        self.speak("Не понял. Доступные команды: привет, как дела, открой браузер, открой панель управления")
        return False
    
    def run(self):
        """Основной цикл"""
        self.speak("Ассистент запущен. Скажите 'привет' для начала.")
        
        while True:
            try:
                # Ждем команду активации
                text = self.listen()
                
                if text and "привет" in text:
                    self.speak("Да, слушаю вас")
                    
                    # Основной режим
                    while True:
                        command = self.listen(timeout=10)
                        
                        if command:
                            result = self.process_command(command)
                            if result == "stop":
                                return
                            
            except KeyboardInterrupt:
                self.speak("Завершение работы")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

# Простая функция для запуска
if __name__ == "__main__":
    assistant = SuperLiteAssistant()
    assistant.run()