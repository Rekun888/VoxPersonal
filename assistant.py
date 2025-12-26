"""
VoxPersonal v6 - Умный ассистент с продвинутыми командами
Команды: 25+ полезных функций
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import os
import time
import pyautogui
import json
import datetime
import random
import requests
import threading
from typing import Optional, Dict, List
import sys
import re

class VoxPersonalV6:
    def __init__(self, gui_callback=None):
        self.name = "Vox Personal v6"
        self.is_listening = False
        self.user_name = None
        self.volume = 50
        self.weather_api_key = None
        self.command_history = []
        self.vox_mode = False
        self.gui_callback = gui_callback  # Callback для GUI
        self.is_active = False
        self.current_command = None
        
        # Расширенные команды
        self.commands = {
            # Базовые
            "привет": self._hello,
            "как дела": self._how_are_you,
            "пока": self._goodbye,
            
            # Системные
            "открой браузер": self._open_browser,
            "закрой браузер": self._close_browser,
            "открой панель управления": self._open_control_panel,
            "запусти командную строку": self._open_cmd,
            "открой диспетчер задач": self._open_task_manager,
            "сделай скриншот": self._take_screenshot,
            
            # Медиа
            "громче": self._volume_up,
            "тише": self._volume_down,
            "стоп": self._media_stop,
            "пауза": self._media_pause_play,
            "продолжи": self._media_pause_play,
            "следующий трек": self._next_track,
            "предыдущий трек": self._previous_track,
            "включи музыку": self._play_music,
            
            # Интернет
            "открой youtube": self._open_youtube,
            "открой вк": self._open_vk,
            "открой сайт": self._open_website,
            "поиск в интернете": self._web_search,
            "какая погода": self._weather,
            "курс валют": self._currency_rate,
            
            # Информационные
            "сколько времени": self._what_time,
            "какая дата": self._what_date,
            "случайное число": self._random_number,
            "расскажи шутку": self._tell_joke,
            "кто ты": self._who_are_you,
            
            # Развлекательные
            "включи кино": self._play_movie,
            "покажи котика": self._show_cat,
            "скажи предсказание": self._fortune_telling,
            
            # Управление
            "выключи компьютер": self._shutdown_pc,
            "перезагрузи компьютер": self._restart_pc,
            "сверни все окна": self._minimize_all,
            "рабочий стол": self._show_desktop,
            
            # Помощь
            "что ты умеешь": self._help,
            "повтори команду": self._repeat_command,
        }
        
        # Синонимы команд
        self.synonyms = {
            "здравствуй": "привет",
            "добрый день": "привет",
            "доброе утро": "привет",
            "добрый вечер": "привет",
            "эй": "привет",
            "слушай": "привет",
            "вокс": "привет",
            
            "как жизнь": "как дела",
            "как ты": "как дела",
            "как сам": "как дела",
            
            "до свидания": "пока",
            "выход": "пока",
            "завершить": "пока",
            
            "браузер": "открой браузер",
            "гугл": "открой браузер",
            "интернет": "открой браузер",
            
            "выключи браузер": "закрой браузер",
            "закрой интернет": "закрой браузер",
            
            "панель управления": "открой панель управления",
            "настройки системы": "открой панель управления",
            
            "командная строка": "запусти командную строку",
            "терминал": "запусти командную строку",
            
            "время": "сколько времени",
            "который час": "сколько времени",
            
            "дата": "какая дата",
            "число": "какая дата",
            "день": "какая дата",
            
            "увеличь громкость": "громче",
            "сделай громче": "громче",
            
            "уменьши громкость": "тише",
            "сделай тише": "тише",
            
            "останови": "стоп",
            "прекрати": "стоп",
            
            "останови музыку": "стоп",
            "прекрати воспроизведение": "стоп",
            
            "поставь на паузу": "пауза",
            "паузи": "пауза",
            
            "возобнови": "продолжи",
            "дальше": "продолжи",
            
            "следующий": "следующий трек",
            "следующая песня": "следующий трек",
            
            "предыдущий": "предыдущий трек",
            "прошлый трек": "предыдущий трек",
            
            "включи видео": "включи музыку",
            "запусти музыку": "включи музыку",
            
            "ютуб": "открой youtube",
            "видео": "открой youtube",
            
            "вконтакте": "открой вк",
            
            "найди в интернете": "поиск в интернете",
            "ищи": "поиск в интернете",
            "гугли": "поиск в интернете",
            
            "прогноз погоды": "какая погода",
            "погода сейчас": "какая погода",
            
            "курс доллара": "курс валют",
            "курс евро": "курс валют",
            "валюты": "курс валют",
            
            "случайное": "случайное число",
            "рандомное число": "случайное число",
            
            "пошути": "расскажи шутку",
            "рассмеши": "расскажи шутку",
            
            "представься": "кто ты",
            "твоё имя": "кто ты",
            
            "включи фильм": "включи кино",
            "посмотреть фильм": "включи кино",
            
            "покажи котёнка": "покажи котика",
            "кот": "покажи котика",
            
            "предскажи": "скажи предсказание",
            "гадание": "скажи предсказание",
            
            "выруби компьютер": "выключи компьютер",
            "отключи компьютер": "выключи компьютер",
            
            "перезагрузка": "перезагрузи компьютер",
            "ребут": "перезагрузи компьютер",
            
            "сверни окна": "сверни все окна",
            "минимизируй всё": "сверни все окна",
            
            "на рабочий стол": "рабочий стол",
            "десктоп": "рабочий стол",
            
            "помощь": "что ты умеешь",
            "команды": "что ты умеешь",
            "функции": "что ты умеешь",
            
            "повтори": "повтори команду",
            "ещё раз": "повтори команду",
        }
        
        # Популярные сайты
        self.websites = {
            "гугл": "https://google.com",
            "яндекс": "https://yandex.ru",
            "почту": "https://gmail.com",
            "почта": "https://gmail.com",
            "гитхаб": "https://github.com",
            "гит": "https://github.com",
            "стековерфлоу": "https://stackoverflow.com",
            "стек": "https://stackoverflow.com",
            "википедию": "https://wikipedia.org",
            "википедия": "https://wikipedia.org",
            "амазон": "https://amazon.com",
            "эппл": "https://apple.com",
            "майкрософт": "https://microsoft.com",
            "фейсбук": "https://facebook.com",
            "инстаграм": "https://instagram.com",
            "твиттер": "https://twitter.com",
            "телеграм": "https://telegram.org",
            "вайбер": "https://viber.com",
            "нетфликс": "https://netflix.com",
            "дискорд": "https://discord.com",
            "редит": "https://reddit.com",
            "линкедин": "https://linkedin.com",
        }
        
        # Инициализация
        self._init_speech()
        self._load_config()
        
    def _init_speech(self):
        """Инициализация голосовых систем"""
        try:
            # Распознавание
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Синтез
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 1.0)
            
            # Русский голос
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'russian' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
                    
            print(f"✅ {self.name} инициализирован")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации: {e}")
    
    def _load_config(self):
        """Загрузка конфигурации"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.user_name = config.get('user_name')
                    self.weather_api_key = config.get('weather_api_key')
                    print("✅ Конфигурация загружена")
        except:
            pass
    
    def _update_gui(self, event_type, data=None):
        """Обновление GUI через callback"""
        if self.gui_callback:
            self.gui_callback(event_type, data)
    
    def speak(self, text, wait=True):
        """Произнести текст"""
        print(f"\n🤖 [{self.name}]: {text}")
        print("─" * 60)
        
        # Обновляем GUI
        self._update_gui('assistant_speak', text)
        
        self.tts_engine.say(text)
        if wait:
            self.tts_engine.runAndWait()
    
    def _show_listening_animation(self):
        """Показать анимацию прослушивания"""
        print("\n" + "█" * 30)
        print(" " * 10 + "🎤 СЛУШАЮ...")
        print("█" * 30)
        
        # Обновляем GUI
        self._update_gui('listening_start', None)
    
    def _show_processing_animation(self):
        """Показать анимацию обработки"""
        print("\n" + "░" * 30)
        print(" " * 10 + "🔍 ОБРАБАТЫВАЮ...")
        print("░" * 30)
        
        # Обновляем GUI
        self._update_gui('processing_start', None)
    
    def _show_recognized_text(self, text):
        """Показать распознанный текст"""
        print("\n📝 РАСПОЗНАНО: ", end="")
        print(f"\033[92m{text}\033[0m")  # Зеленый цвет
        print("─" * 40)
        
        # Обновляем GUI
        self._update_gui('text_recognized', text)
    
    def listen(self, timeout=5, phrase_time_limit=7):
        """Слушать микрофон"""
        try:
            with self.microphone as source:
                # Калибровка фонового шума
                print("\n🔊 Калибровка фонового шума...")
                self._update_gui('calibrating', None)
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Показать анимацию прослушивания
                self._show_listening_animation()
                
                # Запись аудио
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                # Показать анимацию обработки
                self._show_processing_animation()
                
                # Распознавание речи
                print("\n📊 Распознаю команду...")
                text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                
                if text:
                    # Показать распознанный текст
                    self._show_recognized_text(text)
                    return text
                else:
                    self._update_gui('no_speech', None)
                
        except sr.WaitTimeoutError:
            print("\n⏰ Таймаут: голос не обнаружен")
            self._update_gui('timeout', None)
            return None
        except sr.UnknownValueError:
            print("\n❌ Не удалось распознать речь")
            self._update_gui('unknown_value', None)
            return None
        except Exception as e:
            print(f"\n❌ Ошибка слушания: {e}")
            self._update_gui('error', str(e))
            return None
    
    # ===== КОМАНДЫ =====
    
    def _open_website(self, text=""):
        """Открыть сайт по названию или URL"""
        if not text:
            self.speak("Какой сайт открыть?", wait=False)
            query = self.listen()
        else:
            query = text
        
        if query:
            print(f"\n🌐 Поиск сайта: {query}")
            self._update_gui('searching_site', query)
            
            # Проверяем популярные сайты
            for site_name, url in self.websites.items():
                if site_name in query:
                    print(f"✅ Найден сайт: {site_name} -> {url}")
                    self._update_gui('site_found', {'name': site_name, 'url': url})
                    webbrowser.open(url)
                    return f"Открываю {site_name}"
            
            # Пробуем извлечь URL из текста
            url_match = re.search(r'(https?://\S+|www\.\S+\.\w+)', query)
            if url_match:
                url = url_match.group(0)
                if not url.startswith('http'):
                    url = 'https://' + url
                print(f"✅ Найден URL: {url}")
                self._update_gui('url_found', url)
                webbrowser.open(url)
                return f"Открываю {url}"
            
            # Иначе ищем в Google
            print(f"🔍 Не найден, ищу в Google: {query}")
            self._update_gui('searching_google', query)
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Ищу '{query}' в Google"
        
        return "Скажите название сайта"
    
    def _hello(self):
        """Приветствие с именем пользователя"""
        greetings = [
            "Приветствую!",
            "Здравствуйте!",
            "Привет! Рад вас слышать.",
            "Добрый день!",
            "Привет, друг!",
            "Вокс на связи! Чем могу помочь?"
        ]
        
        if self.user_name:
            return f"{random.choice(greetings)} Как ваши дела, {self.user_name}?"
        else:
            return f"{random.choice(greetings)} Меня зовут {self.name}. Как вас зовут?"
    
    def _how_are_you(self):
        """Состояние ассистента"""
        moods = [
            "Всё отлично! Готов помогать.",
            "Прекрасно, как никогда!",
            "Великолепно, спасибо что спросили!",
            "Работаю в полную силу!",
            "Готов к новым задачам!"
        ]
        return random.choice(moods)
    
    def _open_browser(self):
        """Открыть браузер с выбором"""
        print("\n💻 Поиск установленных браузеров...")
        self._update_gui('finding_browsers', None)
        
        browsers = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "opera": r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera\opera.exe"
        }
        
        for name, path in browsers.items():
            try:
                expanded_path = os.path.expandvars(path)
                if os.path.exists(expanded_path):
                    print(f"✅ Найден {name}: {expanded_path}")
                    self._update_gui('browser_found', name)
                    subprocess.Popen([expanded_path])
                    return f"Запускаю {name}"
                else:
                    print(f"❌ {name} не найден")
            except:
                continue
        
        # Если не нашел браузеры, открываем через webbrowser
        print("🌐 Запуск стандартного браузера...")
        self._update_gui('default_browser', None)
        webbrowser.open("https://google.com")
        return "Открываю Google в стандартном браузере"
    
    def _close_browser(self):
        """Закрыть все браузеры (умный способ)"""
        print("\n🛑 Закрытие браузеров...")
        self._update_gui('closing_browsers', None)
        try:
            if os.name == 'nt':  # Windows
                subprocess.run('taskkill /f /im chrome.exe /t', shell=True, capture_output=True)
                subprocess.run('taskkill /f /im firefox.exe /t', shell=True, capture_output=True)
                subprocess.run('taskkill /f /im msedge.exe /t', shell=True, capture_output=True)
                subprocess.run('taskkill /f /im opera.exe /t', shell=True, capture_output=True)
                return "Все браузеры закрыты"
            else:
                return "Используйте диспетчер задач для закрытия браузеров"
        except:
            return "Закройте браузеры вручную через диспетчер задач"
    
    def _open_control_panel(self):
        """Открыть панель управления"""
        try:
            subprocess.run('control', shell=True)
            return "Открываю панель управления Windows"
        except:
            return "Не удалось открыть панель управления"
    
    def _open_cmd(self):
        """Открыть командную строку"""
        try:
            subprocess.Popen('cmd', shell=True)
            return "Запускаю командную строку"
        except:
            return "Не удалось открыть командную строку"
    
    def _open_task_manager(self):
        """Открыть диспетчер задач"""
        try:
            subprocess.Popen('taskmgr', shell=True)
            return "Открываю диспетчер задач"
        except:
            return "Нажмите Ctrl+Shift+Esc для диспетчера задач"
    
    def _take_screenshot(self):
        """Сделать скриншот"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Создаем папку для скриншотов если её нет
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')
            
            filepath = os.path.join('screenshots', filename)
            screenshot.save(filepath)
            print(f"📸 Скриншот сохранен: {filepath}")
            self._update_gui('screenshot_taken', filepath)
            return f"Скриншот сохранён как {filename}"
        except Exception as e:
            return f"Не удалось сделать скриншот: {str(e)}"
    
    def _volume_up(self):
        """Увеличить громкость"""
        try:
            for _ in range(5):
                pyautogui.press('volumeup')
            self.volume = min(100, self.volume + 20)
            print(f"🔊 Громкость увеличена: {self.volume}%")
            self._update_gui('volume_changed', self.volume)
            return f"Громкость: {self.volume}%"
        except:
            return "Используйте кнопки громкости на клавиатуре"
    
    def _volume_down(self):
        """Уменьшить громкость"""
        try:
            for _ in range(5):
                pyautogui.press('volumedown')
            self.volume = max(0, self.volume - 20)
            print(f"🔉 Громкость уменьшена: {self.volume}%")
            self._update_gui('volume_changed', self.volume)
            return f"Громкость: {self.volume}%"
        except:
            return "Используйте кнопки громкости на клавиатуре"
    
    def _media_stop(self):
        """Остановить медиа"""
        try:
            pyautogui.press('stop')
            return "Воспроизведение остановлено"
        except:
            return "Нажмите кнопку стоп в вашем плеере"
    
    def _media_pause_play(self):
        """Пауза/продолжить"""
        try:
            pyautogui.press('playpause')
            return "Переключил воспроизведение"
        except:
            return "Используйте кнопку паузы в вашем плеере"
    
    def _next_track(self):
        """Следующий трек"""
        try:
            pyautogui.hotkey('ctrl', 'right')
            return "Переключаю на следующий трек"
        except:
            return "Используйте Ctrl+→ для следующего трека"
    
    def _previous_track(self):
        """Предыдущий трек"""
        try:
            pyautogui.hotkey('ctrl', 'left')
            return "Переключаю на предыдущий трек"
        except:
            return "Используйте Ctrl+← для предыдущего трека"
    
    def _play_music(self):
        """Включить музыку"""
        try:
            webbrowser.open("https://music.youtube.com")
            return "Включаю YouTube Music"
        except:
            return "Откройте ваш музыкальный сервис"
    
    def _open_youtube(self):
        """Открыть YouTube"""
        webbrowser.open("https://youtube.com")
        return "Открываю YouTube"
    
    def _open_vk(self):
        """Открыть ВКонтакте"""
        webbrowser.open("https://vk.com")
        return "Открываю ВКонтакте"
    
    def _web_search(self):
        """Поиск в интернете"""
        self.speak("Что искать в интернете?", wait=False)
        query = self.listen()
        if query:
            print(f"🔍 Поиск в Google: {query}")
            self._update_gui('web_search', query)
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Ищу '{query}' в Google"
        return "Скажите что искать"
    
    def _weather(self):
        """Погода (заглушка - можно подключить API)"""
        cities = ["Москве", "Санкт-Петербурге", "Новосибирске", "Екатеринбурге"]
        temps = random.randint(-10, 30)
        conditions = ["солнечно", "облачно", "дождливо", "снежно", "пасмурно"]
        
        city = random.choice(cities)
        condition = random.choice(conditions)
        
        print(f"🌤️ Погода в {city}: {temps}°C, {condition}")
        self._update_gui('weather_info', {'city': city, 'temp': temps, 'condition': condition})
        return f"В {city} сейчас {temps}°C, {condition}. Для точного прогноза скажите 'установи ключ погоды'"
    
    def _currency_rate(self):
        """Курс валют (заглушка)"""
        usd = round(random.uniform(70, 90), 2)
        eur = round(random.uniform(75, 95), 2)
        print(f"💱 Курс валют: USD = {usd} RUB, EUR = {eur} RUB")
        self._update_gui('currency_info', {'usd': usd, 'eur': eur})
        return f"Курс доллара: {usd} руб., евро: {eur} руб. Данные приблизительные"
    
    def _what_time(self):
        """Текущее время"""
        now = datetime.datetime.now()
        time_str = now.strftime('%H:%M')
        print(f"🕐 Текущее время: {time_str}")
        self._update_gui('time_info', time_str)
        return f"Сейчас {time_str}"
    
    def _what_date(self):
        """Текущая дата"""
        now = datetime.datetime.now()
        months = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]
        date_str = f"{now.day} {months[now.month-1]} {now.year} года"
        print(f"📅 Текущая дата: {date_str}")
        self._update_gui('date_info', date_str)
        return f"Сегодня {date_str}"
    
    def _random_number(self):
        """Случайное число"""
        num = random.randint(1, 100)
        print(f"🎲 Случайное число: {num}")
        self._update_gui('random_number', num)
        return f"Ваше случайное число: {num}"
    
    def _tell_joke(self):
        """Рассказать шутку"""
        jokes = [
            "Почему программист всегда мокрый? Потому что он постоянно в бассейне кода!",
            "Что сказал один массив другому? Привет, я твой отец!",
            "Почему Python не может полюбить? Потому что у него нет сердца, только интерпретатор!",
            "Какой язык программирования самый романтичный? Любви-Скрипт!",
            "Зачем программисту зеркало? Чтобы посмотреть на свой отраженный код!",
            "Что говорит null, когда встречает undefined? Ты мне не определен!",
            "Почему компьютер пошёл к врачу? У него был вирус!",
        ]
        joke = random.choice(jokes)
        print(f"😂 Шутка: {joke}")
        self._update_gui('joke_told', joke)
        return joke
    
    def _who_are_you(self):
        """Представление ассистента"""
        return f"Я {self.name}, ваш персональный голосовой помощник. Я умею управлять компьютером, искать информацию в интернете, рассказывать шутки и многое другое!"
    
    def _play_movie(self):
        """Включить кино"""
        platforms = ["https://www.netflix.com", "https://www.kinopoisk.ru", "https://www.ivi.ru"]
        platform = random.choice(platforms)
        print(f"🎬 Открываю платформу: {platform}")
        self._update_gui('movie_platform', platform)
        webbrowser.open(platform)
        return "Открываю платформу для просмотра фильмов"
    
    def _show_cat(self):
        """Показать котика"""
        webbrowser.open("https://thecatapi.com/api/images/get?format=src&type=gif")
        return "Смотрите на этого милого котика!"
    
    def _fortune_telling(self):
        """Предсказание"""
        fortunes = [
            "Сегодня вас ждёт удача в программировании!",
            "Вскоре вы найдёте баг, который искали месяц.",
            "Сегодня отличный день для изучения нового фреймворка!",
            "Вас ждёт интересная задача на работе.",
            "Не бойтесь пробовать новые технологии сегодня!",
            "Ваш код сегодня будет работать с первого раза!",
        ]
        fortune = random.choice(fortunes)
        print(f"🔮 Предсказание: {fortune}")
        self._update_gui('fortune_told', fortune)
        return fortune
    
    def _shutdown_pc(self):
        """Выключить компьютер"""
        self.speak("Вы уверены что хотите выключить компьютер? Скажите да или нет")
        confirm = self.listen()
        if confirm and "да" in confirm:
            if os.name == 'nt':
                os.system("shutdown /s /t 30")
                return "Компьютер выключится через 30 секунд. Для отмены скажите 'отмена выключения'"
            else:
                return "Используйте команду 'sudo shutdown now' в терминале"
        return "Выключение отменено"
    
    def _restart_pc(self):
        """Перезагрузить компьютер"""
        if os.name == 'nt':
            os.system("shutdown /r /t 30")
            return "Перезагрузка через 30 секунд"
        return "Перезагрузите компьютер через меню Пуск"
    
    def _minimize_all(self):
        """Свернуть все окна"""
        pyautogui.hotkey('win', 'd')
        return "Все окна свернуты"
    
    def _show_desktop(self):
        """Показать рабочий стол"""
        pyautogui.hotkey('win', 'd')
        return "Показываю рабочий стол"
    
    def _help(self):
        """Показать список команд"""
        categories = {
            "🎯 Базовые": ["привет", "вокс (активация)", "как дела", "пока"],
            "💻 Система": ["открой браузер", "закрой браузер", "открой панель управления", "сделай скриншот"],
            "🌐 Сайты": ["открой сайт [название]", "открой youtube", "открой вк", "поиск в интернете"],
            "🎵 Медиа": ["громче", "тише", "стоп", "пауза", "следующий трек", "включи музыку"],
            "📅 Информация": ["сколько времени", "какая дата", "случайное число", "расскажи шутку"],
            "🎮 Развлечения": ["включи кино", "покажи котика", "скажи предсказание"],
            "⚙️ Управление": ["выключи компьютер", "сверни все окна", "рабочий стол"]
        }
        
        response = "Я умею многое! Вот основные команды:\n\n"
        for category, commands in categories.items():
            response += f"{category}:\n"
            for cmd in commands:
                response += f"  • {cmd}\n"
            response += "\n"
        
        response += "Просто скажите 'вокс' или 'привет' для начала общения!"
        
        # Отправляем категории в GUI
        self._update_gui('help_commands', categories)
        
        print("\n📋 СПИСОК КОМАНД:")
        for category, commands in categories.items():
            print(f"\n{category}:")
            for cmd in commands:
                print(f"  • {cmd}")
        return response
    
    def _repeat_command(self):
        """Повторить последнюю команду"""
        if self.command_history:
            last_cmd = self.command_history[-1]
            print(f"🔄 Повтор команды: {last_cmd}")
            self._update_gui('repeat_command', last_cmd)
            return f"Повторяю последнюю команду: '{last_cmd}'"
        return "История команд пуста"
    
    def _goodbye(self):
        """Прощание"""
        farewells = [
            "До свидания! Буду рад помочь снова.",
            "Пока! Обращайтесь если что.",
            "Всего хорошего!",
            "До встречи!",
            "Пока, не скучайте!"
        ]
        self.is_listening = False
        self.vox_mode = False
        self.is_active = False
        self._update_gui('assistant_off', None)
        return random.choice(farewells)
    
    def process_command(self, text):
        """Обработка команды"""
        if not text:
            return None
        
        # Сохраняем в историю
        self.command_history.append(text[:50])
        print(f"\n📚 История команд: {self.command_history[-3:]}")
        self._update_gui('command_history', self.command_history[-3:])
        
        # Обработка команды "открой сайт"
        if "открой сайт" in text:
            site_query = text.replace("открой сайт", "").strip()
            return self._open_website(site_query)
        
        # Проверяем точное совпадение
        for cmd, func in self.commands.items():
            if cmd in text:
                print(f"🎯 Найдена команда: {cmd}")
                self.current_command = cmd
                self._update_gui('command_found', cmd)
                return func()
        
        # Проверяем синонимы
        for synonym, command in self.synonyms.items():
            if synonym in text and command in self.commands:
                print(f"🔍 Синоним: {synonym} -> {command}")
                self.current_command = command
                self._update_gui('synonym_used', {'synonym': synonym, 'command': command})
                return self.commands[command]()
        
        # Режим "Вокс" - пользователь говорит "Вокс" + команда
        if "вокс" in text:
            # Извлекаем команду после "вокс"
            command_part = text.replace("вокс", "").strip()
            if command_part:
                for cmd, func in self.commands.items():
                    if cmd in command_part:
                        print(f"🎯 Вокс-команда: {cmd}")
                        self.current_command = cmd
                        self._update_gui('vox_command', cmd)
                        return func()
            
            # Если просто "вокс" без команды, активируем режим
            self.vox_mode = True
            self.is_active = True
            self._update_gui('vox_mode_on', None)
            return "Слушаю вас! Говорите команду."
        
        # Режим "Вокс" активирован - обрабатываем как команду
        if self.vox_mode and text:
            for cmd, func in self.commands.items():
                if cmd in text:
                    print(f"🎯 Вокс-режим: {cmd}")
                    self.current_command = cmd
                    self._update_gui('vox_mode_command', cmd)
                    return func()
            # Если не нашли команду, проверяем синонимы
            for synonym, command in self.synonyms.items():
                if synonym in text and command in self.commands:
                    print(f"🔍 Вокс-синоним: {synonym} -> {command}")
                    self.current_command = command
                    self._update_gui('vox_synonym', {'synonym': synonym, 'command': command})
                    return self.commands[command]()
        
        # Установка имени пользователя
        if "меня зовут" in text:
            name = text.split("меня зовут")[-1].strip()
            self.user_name = name
            print(f"👤 Установлено имя: {name}")
            self._update_gui('user_name_set', name)
            return f"Приятно познакомиться, {name}!"
        
        # Если не распознали
        responses = [
            "Извините, не понял команду. Попробуйте сказать 'что ты умеешь'",
            "Не распознал команду. Скажите 'помощь' для списка команд",
            "Повторите, пожалуйста, я не понял",
            "Можете повторить команду?"
        ]
        response = random.choice(responses)
        print(f"❌ Не распознано: {text}")
        self._update_gui('command_not_recognized', text)
        return response
    
    def run(self):
        """Основной цикл работы"""
        print("\n" + "=" * 60)
        print("🤖 VoxPersonal v6 - Умный голосовой помощник")
        print("=" * 60)
        
        self.speak(f"{self.name} запущен. Скажите 'вокс' или 'привет' для начала общения!")
        
        while True:
            try:
                # Ждем активации
                print("\n" + "━" * 40)
                print("⏳ ЖДУ АКТИВАЦИИ... (скажите 'вокс' или 'привет')")
                print("━" * 40)
                self._update_gui('waiting_activation', None)
                text = self.listen()
                
                if text and any(word in text for word in ["привет", "эй", "окей", "слушай", "компьютер", "вокс"]):
                    print("\n🚀 АКТИВАЦИЯ УСПЕШНА!")
                    self.is_active = True
                    self._update_gui('activated', None)
                    response = self.process_command(text)
                    if response:
                        self.speak(response)
                    
                    # Режим активного слушания
                    while self.is_active:
                        print("\n" + "━" * 40)
                        print("📝 ОЖИДАЮ КОМАНДУ... (скажите 'пока' для выхода)")
                        print("━" * 40)
                        self._update_gui('waiting_command', None)
                        command = self.listen()
                        
                        if command:
                            if "пока" in command or "выход" in command:
                                response = self.process_command(command)
                                self.speak(response)
                                break
                            
                            response = self.process_command(command)
                            if response:
                                self.speak(response)
                        
                        time.sleep(0.5)
                        
                elif text:
                    # Попробуем обработать без активации
                    response = self.process_command(text)
                    if response:
                        self.speak(response)
                        
            except KeyboardInterrupt:
                print("\n\n🛑 Прерывание пользователем")
                self.speak("Работа завершена")
                self._update_gui('interrupted', None)
                break
            except Exception as e:
                print(f"\n❌ Критическая ошибка: {e}")
                self._update_gui('critical_error', str(e))
                time.sleep(1)

if __name__ == "__main__":
    assistant = VoxPersonalV6()
    assistant.run()