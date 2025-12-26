"""
VoxPersonal v6 - Графический интерфейс с боковым меню
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from PIL import Image, ImageTk
import sys
from assistant import VoxPersonalV6

class VoxPersonalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VoxPersonal v6 - Умный голосовой помощник")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Стили
        self.setup_styles()
        
        # Создаем иконку для окна (если файл существует)
        try:
            self.root.iconbitmap("icons/logo.ico")
        except:
            pass
        
        # Инициализация помощника
        self.assistant = VoxPersonalV6(gui_callback=self.update_gui)
        self.is_running = False
        self.assistant_thread = None
        
        # Создание интерфейса
        self.setup_ui()
        
        # Загрузка конфигурации
        self.load_config()
        
        # Центрирование окна
        self.center_window()
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        self.style = ttk.Style()
        
        # Современная тема
        self.style.theme_use('clam')
        
        # Цветовая схема
        self.colors = {
            'primary': '#4a6fa5',
            'secondary': '#6c8bc7',
            'success': '#5cb85c',
            'danger': '#d9534f',
            'warning': '#f0ad4e',
            'info': '#5bc0de',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'sidebar': '#2c3e50',
            'header': '#34495e',
            'active': '#3498db'
        }
        
        # Настройка стилей
        self.style.configure('Sidebar.TFrame', background=self.colors['sidebar'])
        self.style.configure('Content.TFrame', background=self.colors['light'])
        self.style.configure('Header.TLabel', 
                           background=self.colors['header'],
                           foreground='white',
                           font=('Segoe UI', 16, 'bold'))
        self.style.configure('Button.TButton',
                           padding=10,
                           font=('Segoe UI', 10))
    
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Главный контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Боковая панель
        self.setup_sidebar(main_container)
        
        # Основное содержимое
        self.setup_content(main_container)
        
        # Статус бар
        self.setup_statusbar()
    
    def setup_sidebar(self, parent):
        """Создание боковой панели"""
        sidebar = ttk.Frame(parent, width=200, style='Sidebar.TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Логотип
        logo_frame = ttk.Frame(sidebar)
        logo_frame.pack(pady=20)
        
        try:
            # Пробуем загрузить логотип
            img = Image.open("icons/logo.png")
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(logo_frame, image=self.logo_img, background=self.colors['sidebar'])
            logo_label.pack()
        except:
            # Если иконки нет, используем текст
            logo_label = ttk.Label(logo_frame, 
                                 text="🤖 Vox\nPersonal",
                                 font=('Segoe UI', 14, 'bold'),
                                 background=self.colors['sidebar'],
                                 foreground='white',
                                 justify=tk.CENTER)
            logo_label.pack()
        
        # Разделитель
        separator = ttk.Separator(sidebar, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопки навигации
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Главная", "home"),
            ("👤 Аккаунт", "account"),
            ("⚙️ Настройки", "settings"),
            ("🎤 Команды", "commands"),
            ("📊 Статистика", "stats"),
            ("❓ Помощь", "help")
        ]
        
        for text, command in nav_items:
            btn = tk.Button(sidebar,
                          text=text,
                          font=('Segoe UI', 11),
                          bg=self.colors['sidebar'],
                          fg='white',
                          bd=0,
                          padx=20,
                          pady=12,
                          anchor='w',
                          command=lambda cmd=command: self.show_page(cmd))
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.nav_buttons[command] = btn
        
        # Кнопка запуска/остановки
        self.start_btn = tk.Button(sidebar,
                                 text="▶️ Запустить помощника",
                                 font=('Segoe UI', 11, 'bold'),
                                 bg=self.colors['success'],
                                 fg='white',
                                 bd=0,
                                 padx=20,
                                 pady=15,
                                 command=self.toggle_assistant)
        self.start_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=20)
    
    def setup_content(self, parent):
        """Создание основного контента"""
        # Контейнер для контента
        self.content_frame = ttk.Frame(parent, style='Content.TFrame')
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Создаем страницы
        self.pages = {}
        self.create_home_page()
        self.create_account_page()
        self.create_settings_page()
        self.create_commands_page()
        self.create_stats_page()
        self.create_help_page()
        
        # Показываем главную страницу по умолчанию
        self.show_page('home')
    
    def create_home_page(self):
        """Создание главной страницы"""
        page = ttk.Frame(self.content_frame)
        self.pages['home'] = page
        
        # Заголовок
        header = ttk.Label(page, 
                          text="🏠 Добро пожаловать в VoxPersonal v6!",
                          font=('Segoe UI', 24, 'bold'),
                          background=self.colors['light'])
        header.pack(pady=30)
        
        # Основной контент
        content_frame = ttk.Frame(page, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая колонка - статус
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        status_card = self.create_card(left_frame, "📊 Статус системы")
        self.status_label = ttk.Label(status_card, 
                                     text="⏸️ Помощник остановлен",
                                     font=('Segoe UI', 12))
        self.status_label.pack(pady=10)
        
        # Индикатор активности
        self.active_indicator = tk.Canvas(status_card, width=30, height=30, bg='white', highlightthickness=0)
        self.active_indicator.pack(pady=10)
        self.update_indicator('off')
        
        # Кнопка микрофона
        mic_btn = tk.Button(status_card,
                          text="🎤 Произнести команду",
                          font=('Segoe UI', 11),
                          bg=self.colors['primary'],
                          fg='white',
                          padx=20,
                          pady=10,
                          command=self.speak_command)
        mic_btn.pack(pady=20)
        
        # Правая колонка - последние действия
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        actions_card = self.create_card(right_frame, "📝 Последние действия")
        
        # Текстовое поле для логов
        self.log_text = scrolledtext.ScrolledText(actions_card,
                                                height=10,
                                                font=('Consolas', 10),
                                                bg='white')
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.log_text.config(state=tk.DISABLED)
        
        # Очистить логи
        clear_btn = tk.Button(actions_card,
                            text="🗑️ Очистить логи",
                            font=('Segoe UI', 10),
                            bg=self.colors['danger'],
                            fg='white',
                            padx=15,
                            pady=5,
                            command=self.clear_logs)
        clear_btn.pack(pady=5)
        
        # Быстрые команды
        commands_card = self.create_card(content_frame, "⚡ Быстрые команды")
        
        quick_commands = [
            ("⏰ Время", "сколько времени"),
            ("📅 Дата", "какая дата"),
            ("🌤️ Погода", "какая погода"),
            ("😂 Шутка", "расскажи шутку"),
            ("🌐 Браузер", "открой браузер")
        ]
        
        for text, command in quick_commands:
            btn = tk.Button(commands_card,
                          text=text,
                          font=('Segoe UI', 10),
                          bg=self.colors['info'],
                          fg='white',
                          padx=15,
                          pady=5,
                          command=lambda cmd=command: self.execute_command(cmd))
            btn.pack(side=tk.LEFT, padx=5, pady=10)
    
    def create_account_page(self):
        """Создание страницы аккаунта"""
        page = ttk.Frame(self.content_frame)
        self.pages['account'] = page
        
        # Заголовок
        header = ttk.Label(page, 
                          text="👤 Ваш аккаунт",
                          font=('Segoe UI', 24, 'bold'),
                          background=self.colors['light'])
        header.pack(pady=30)
        
        # Форма профиля
        profile_card = self.create_card(page, "👤 Профиль пользователя")
        
        ttk.Label(profile_card, text="Ваше имя:", font=('Segoe UI', 11)).pack(pady=5)
        self.name_entry = ttk.Entry(profile_card, font=('Segoe UI', 11), width=30)
        self.name_entry.pack(pady=5)
        
        if self.assistant.user_name:
            self.name_entry.insert(0, self.assistant.user_name)
        
        save_btn = tk.Button(profile_card,
                           text="💾 Сохранить",
                           font=('Segoe UI', 11),
                           bg=self.colors['success'],
                           fg='white',
                           padx=20,
                           pady=10,
                           command=self.save_profile)
        save_btn.pack(pady=20)
        
        # Статистика
        stats_card = self.create_card(page, "📊 Статистика использования")
        
        self.stats_labels = {}
        stats_data = [
            ("Всего команд:", "0"),
            ("Успешных:", "0"),
            ("Ошибок:", "0"),
            ("Время работы:", "0 мин")
        ]
        
        for label_text, value in stats_data:
            frame = ttk.Frame(stats_card)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=label_text, font=('Segoe UI', 11), width=15).pack(side=tk.LEFT)
            label = ttk.Label(frame, text=value, font=('Segoe UI', 11, 'bold'))
            label.pack(side=tk.LEFT)
            self.stats_labels[label_text] = label
    
    def create_settings_page(self):
        """Создание страницы настроек"""
        page = ttk.Frame(self.content_frame)
        self.pages['settings'] = page
        
        # Заголовок
        header = ttk.Label(page, 
                          text="⚙️ Настройки",
                          font=('Segoe UI', 24, 'bold'),
                          background=self.colors['light'])
        header.pack(pady=30)
        
        # Настройки голоса
        voice_card = self.create_card(page, "🔊 Настройки голоса")
        
        ttk.Label(voice_card, text="Скорость речи:", font=('Segoe UI', 11)).pack(pady=5)
        self.speed_scale = ttk.Scale(voice_card, from_=100, to=300, orient=tk.HORIZONTAL)
        self.speed_scale.set(180)
        self.speed_scale.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(voice_card, text="Громкость:", font=('Segoe UI', 11)).pack(pady=5)
        self.volume_scale = ttk.Scale(voice_card, from_=0, to=100, orient=tk.HORIZONTAL)
        self.volume_scale.set(self.assistant.volume)
        self.volume_scale.pack(fill=tk.X, padx=20, pady=5)
        
        # Настройки распознавания
        recog_card = self.create_card(page, "🎤 Настройки распознавания")
        
        self.auto_start_var = tk.BooleanVar()
        auto_start_check = ttk.Checkbutton(recog_card, 
                                         text="Автозапуск при старте",
                                         variable=self.auto_start_var)
        auto_start_check.pack(pady=5)
        
        self.voice_activation_var = tk.BooleanVar(value=True)
        voice_activation_check = ttk.Checkbutton(recog_card, 
                                               text="Голосовая активация",
                                               variable=self.voice_activation_var)
        voice_activation_check.pack(pady=5)
        
        # Кнопки сохранения
        save_btn = tk.Button(page,
                           text="💾 Сохранить настройки",
                           font=('Segoe UI', 11),
                           bg=self.colors['success'],
                           fg='white',
                           padx=20,
                           pady=10,
                           command=self.save_settings)
        save_btn.pack(pady=20)
    
    def create_commands_page(self):
        """Создание страницы команд"""
        page = ttk.Frame(self.content_frame)
        self.pages['commands'] = page
        
        # Заголовок
        header = ttk.Label(page, 
                          text="🎤 Доступные команды",
                          font=('Segoe UI', 24, 'bold'),
                          background=self.colors['light'])
        header.pack(pady=30)
        
        # Фильтр команд
        filter_frame = ttk.Frame(page)
        filter_frame.pack(pady=10)
        
        ttk.Label(filter_frame, text="Поиск команд:", font=('Segoe UI', 11)).pack(side=tk.LEFT, padx=5)
        self.command_filter = ttk.Entry(filter_frame, font=('Segoe UI', 11), width=30)
        self.command_filter.pack(side=tk.LEFT, padx=5)
        self.command_filter.bind('<KeyRelease>', self.filter_commands)
        
        # Список команд
        commands_frame = ttk.Frame(page)
        commands_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview для команд
        columns = ('Категория', 'Команда', 'Описание')
        self.commands_tree = ttk.Treeview(commands_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.commands_tree.heading(col, text=col)
            self.commands_tree.column(col, width=200)
        
        self.commands_tree.pack(fill=tk.BOTH, expand=True)
        
        # Заполняем команды
        self.populate_commands()
        
        # Кнопка выполнения
        exec_btn = tk.Button(page,
                           text="▶️ Выполнить выбранную команду",
                           font=('Segoe UI', 11),
                           bg=self.colors['primary'],
                           fg='white',
                           padx=20,
                           pady=10,
                           command=self.execute_selected_command)
        exec_btn.pack(pady=10)
    
    def create_stats_page(self):
        """Создание страницы статистики"""
        page = ttk.Frame(self.content_frame)
        self.pages['stats'] = page
        
        # Заголовок
        header = ttk.Label(page, 
                          text="📊 Статистика использования",
                          font=('Segoe UI', 24, 'bold'),
                          background=self.colors['light'])
        header.pack(pady=30)
        
        # Графики статистики (заглушки)
        stats_card = self.create_card(page, "📈 Динамика использования")
        
        # Здесь можно добавить реальные графики с помощью matplotlib
        placeholder = tk.Label(stats_card, 
                             text="📊 Графики статистики будут отображаться здесь",
                             font=('Segoe UI', 12),
                             bg='white')
        placeholder.pack(pady=50)
        
        # Детальная статистика
        detail_card = self.create_card(page, "📋 Детальная статистика")
        
        self.stats_text = scrolledtext.ScrolledText(detail_card,
                                                  height=8,
                                                  font=('Consolas', 10),
                                                  bg='white')
        self.stats_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.stats_text.insert('1.0', 'Статистика появится после использования помощника')
        self.stats_text.config(state=tk.DISABLED)
    
    def create_help_page(self):
        """Создание страницы помощи"""
        page = ttk.Frame(self.content_frame)
        self.pages['help'] = page
        
        # Заголовок
        header = ttk.Label(page, 
                          text="❓ Помощь и поддержка",
                          font=('Segoe UI', 24, 'bold'),
                          background=self.colors['light'])
        header.pack(pady=30)
        
        # FAQ
        faq_card = self.create_card(page, "❔ Часто задаваемые вопросы")
        
        faq_text = """🤖 Как активировать помощника?
• Скажите "Вокс" или "Привет"
• Или нажмите кнопку "Запустить помощника"

🎤 Как говорить команды?
• Четко произносите команды на русском языке
• Используйте микрофон хорошего качества

🌐 Какие сайты можно открывать?
• Все популярные сайты: YouTube, ВК, GitHub и т.д.
• Или просто скажите "Открой сайт [название]"

⚙️ Где найти все команды?
• Перейдите на вкладку "Команды"
• Или скажите "Что ты умеешь"

🔧 Нет звука или не работает микрофон?
• Проверьте подключение устройств
• Запустите программу от имени администратора"""
        
        help_text = scrolledtext.ScrolledText(faq_card,
                                            height=15,
                                            font=('Segoe UI', 10),
                                            bg='white',
                                            wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True, pady=10)
        help_text.insert('1.0', faq_text)
        help_text.config(state=tk.DISABLED)
        
        # Контакты поддержки
        contact_card = self.create_card(page, "📞 Контакты поддержки")
        
        contact_info = """📧 Email: support@voxpersonal.com
🌐 Веб-сайт: https://voxpersonal.com
💬 Telegram: @voxpersonal_support

🕐 Часы работы поддержки:
Пн-Пт: 9:00-18:00
Сб-Вс: 10:00-16:00"""
        
        contact_label = tk.Label(contact_card,
                               text=contact_info,
                               font=('Segoe UI', 11),
                               bg='white',
                               justify=tk.LEFT)
        contact_label.pack(pady=10)
    
    def create_card(self, parent, title):
        """Создание карточки с заголовком"""
        card = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        card.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        # Заголовок карточки
        header = tk.Frame(card, bg=self.colors['primary'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header,
                             text=title,
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['primary'],
                             fg='white')
        title_label.pack(pady=10)
        
        # Контент карточки
        content = tk.Frame(card, bg='white', padx=20, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        return content
    
    def setup_statusbar(self):
        """Создание статус бара"""
        self.statusbar = ttk.Frame(self.root, height=25)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.statusbar.pack_propagate(False)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов к работе")
        status_label = ttk.Label(self.statusbar, 
                               textvariable=self.status_var,
                               font=('Segoe UI', 9))
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Версия
        version_label = ttk.Label(self.statusbar,
                                text="VoxPersonal v6.0",
                                font=('Segoe UI', 9))
        version_label.pack(side=tk.RIGHT, padx=10)
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_page(self, page_name):
        """Показать выбранную страницу"""
        # Скрыть все страницы
        for page in self.pages.values():
            page.pack_forget()
        
        # Показать выбранную страницу
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        
        # Обновить стиль активной кнопки
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.config(bg=self.colors['active'])
            else:
                btn.config(bg=self.colors['sidebar'])
    
    def toggle_assistant(self):
        """Запуск/остановка помощника"""
        if not self.is_running:
            self.start_assistant()
        else:
            self.stop_assistant()
    
    def start_assistant(self):
        """Запуск помощника в отдельном потоке"""
        self.is_running = True
        self.start_btn.config(text="⏸️ Остановить помощника", bg=self.colors['danger'])
        self.status_var.set("Помощник запущен...")
        self.update_indicator('on')
        self.add_log("🚀 Помощник запущен")
        
        # Запуск в отдельном потоке
        self.assistant_thread = threading.Thread(target=self.assistant.run, daemon=True)
        self.assistant_thread.start()
    
    def stop_assistant(self):
        """Остановка помощника"""
        self.is_running = False
        self.start_btn.config(text="▶️ Запустить помощника", bg=self.colors['success'])
        self.status_var.set("Помощник остановлен")
        self.update_indicator('off')
        self.add_log("⏸️ Помощник остановлен")
        
        # Отправляем команду выхода
        self.assistant.is_active = False
    
    def update_indicator(self, state):
        """Обновление индикатора активности"""
        self.active_indicator.delete("all")
        
        if state == 'on':
            color = 'green'
            text = "ОН"
        elif state == 'listening':
            color = 'orange'
            text = "СЛУШАЮ"
        elif state == 'processing':
            color = 'blue'
            text = "ОБРАБАТЫВАЮ"
        else:
            color = 'red'
            text = "ВЫКЛ"
        
        # Рисуем круг
        self.active_indicator.create_oval(5, 5, 25, 25, fill=color, outline='black')
        # Рисуем текст
        self.active_indicator.create_text(15, 40, text=text, font=('Arial', 8))
    
    def add_log(self, message):
        """Добавление сообщения в лог"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_logs(self):
        """Очистка логов"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.add_log("🗑️ Логи очищены")
    
    def speak_command(self):
        """Запуск распознавания команды"""
        if not self.is_running:
            messagebox.showwarning("Внимание", "Запустите помощник сначала!")
            return
        
        self.add_log("🎤 Запрос команды...")
        self.update_indicator('listening')
        
        # В реальном приложении здесь будет запуск распознавания
        # Сейчас это заглушка
        self.root.after(2000, self.process_mock_command)
    
    def process_mock_command(self):
        """Обработка тестовой команды (заглушка)"""
        self.update_indicator('processing')
        self.add_log("🎯 Распознано: 'сколько времени'")
        
        # Имитация обработки
        self.root.after(1000, lambda: self.add_log("🤖 Ответ: Сейчас 14:30"))
        self.root.after(1000, lambda: self.update_indicator('on'))
    
    def execute_command(self, command):
        """Выполнение команды напрямую"""
        if not self.is_running:
            messagebox.showwarning("Внимание", "Запустите помощник сначала!")
            return
        
        self.add_log(f"⚡ Выполнение команды: '{command}'")
        self.assistant.process_command(command)
    
    def execute_selected_command(self):
        """Выполнение выбранной команды из списка"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showinfo("Выбор команды", "Выберите команду из списка")
            return
        
        item = self.commands_tree.item(selection[0])
        command = item['values'][1]  # Второй столбец - команда
        
        if command and self.is_running:
            self.execute_command(command)
    
    def populate_commands(self):
        """Заполнение списка команд"""
        commands = [
            ("🎯 Базовые", "привет", "Активация помощника"),
            ("🎯 Базовые", "вокс", "Голосовая активация"),
            ("🎯 Базовые", "как дела", "Статус помощника"),
            ("🎯 Базовые", "пока", "Завершение работы"),
            
            ("💻 Система", "открой браузер", "Запуск браузера"),
            ("💻 Система", "закрой браузер", "Закрытие браузера"),
            ("💻 Система", "сделай скриншот", "Создание скриншота"),
            ("💻 Система", "открой панель управления", "Панель управления"),
            
            ("🌐 Сайты", "открой сайт [название]", "Открытие сайта"),
            ("🌐 Сайты", "открой youtube", "YouTube"),
            ("🌐 Сайты", "открой вк", "ВКонтакте"),
            ("🌐 Сайты", "поиск в интернете", "Поиск в Google"),
            
            ("🎵 Медиа", "громче", "Увеличить громкость"),
            ("🎵 Медиа", "тише", "Уменьшить громкость"),
            ("🎵 Медиа", "стоп", "Остановить воспроизведение"),
            ("🎵 Медиа", "пауза", "Пауза/продолжить"),
            
            ("📅 Информация", "сколько времени", "Текущее время"),
            ("📅 Информация", "какая дата", "Текущая дата"),
            ("📅 Информация", "случайное число", "Случайное число"),
            ("📅 Информация", "расскажи шутку", "Рассказать шутку"),
            
            ("🎮 Развлечения", "включи кино", "Фильмы онлайн"),
            ("🎮 Развлечения", "покажи котика", "Случайный кот"),
            ("🎮 Развлечения", "скажи предсказание", "Предсказание"),
            
            ("⚙️ Управление", "выключи компьютер", "Выключение ПК"),
            ("⚙️ Управление", "сверни все окна", "Свернуть окна"),
            ("⚙️ Управление", "рабочий стол", "Показать рабочий стол"),
        ]
        
        for category, command, description in commands:
            self.commands_tree.insert('', tk.END, values=(category, command, description))
    
    def filter_commands(self, event):
        """Фильтрация команд по введенному тексту"""
        filter_text = self.command_filter.get().lower()
        
        # Удаляем все элементы
        for item in self.commands_tree.get_children():
            self.commands_tree.delete(item)
        
        # Заново заполняем отфильтрованные команды
        commands = [
            ("🎯 Базовые", "привет", "Активация помощника"),
            ("🎯 Базовые", "вокс", "Голосовая активация"),
            ("🎯 Базовые", "как дела", "Статус помощника"),
            ("🎯 Базовые", "пока", "Завершение работы"),
            
            ("💻 Система", "открой браузер", "Запуск браузера"),
            ("💻 Система", "закрой браузер", "Закрытие браузера"),
            ("💻 Система", "сделай скриншот", "Создание скриншота"),
            ("💻 Система", "открой панель управления", "Панель управления"),
            
            ("🌐 Сайты", "открой сайт [название]", "Открытие сайта"),
            ("🌐 Сайты", "открой youtube", "YouTube"),
            ("🌐 Сайты", "открой вк", "ВКонтакте"),
            ("🌐 Сайты", "поиск в интернете", "Поиск в Google"),
            
            ("🎵 Медиа", "громче", "Увеличить громкость"),
            ("🎵 Медиа", "тише", "Уменьшить громкость"),
            ("🎵 Медиа", "стоп", "Остановить воспроизведение"),
            ("🎵 Медиа", "пауза", "Пауза/продолжить"),
            
            ("📅 Информация", "сколько времени", "Текущее время"),
            ("📅 Информация", "какая дата", "Текущая дата"),
            ("📅 Информация", "случайное число", "Случайное число"),
            ("📅 Информация", "расскажи шутку", "Рассказать шутку"),
            
            ("🎮 Развлечения", "включи кино", "Фильмы онлайн"),
            ("🎮 Развлечения", "покажи котика", "Случайный кот"),
            ("🎮 Развлечения", "скажи предсказание", "Предсказание"),
            
            ("⚙️ Управление", "выключи компьютер", "Выключение ПК"),
            ("⚙️ Управление", "сверни все окна", "Свернуть окна"),
            ("⚙️ Управление", "рабочий стол", "Показать рабочий стол"),
        ]
        
        for category, command, description in commands:
            if (filter_text in category.lower() or 
                filter_text in command.lower() or 
                filter_text in description.lower()):
                self.commands_tree.insert('', tk.END, values=(category, command, description))
    
    def save_profile(self):
        """Сохранение профиля пользователя"""
        name = self.name_entry.get().strip()
        if name:
            self.assistant.user_name = name
            self.add_log(f"👤 Имя пользователя сохранено: {name}")
            messagebox.showinfo("Успех", f"Имя пользователя сохранено: {name}")
            
            # Сохраняем в конфиг
            self.save_config()
        else:
            messagebox.showwarning("Внимание", "Введите имя пользователя")
    
    def save_settings(self):
        """Сохранение настроек"""
        # Сохраняем настройки голоса
        self.assistant.tts_engine.setProperty('rate', self.speed_scale.get())
        self.assistant.volume = int(self.volume_scale.get())
        
        # Сохраняем конфигурацию
        self.save_config()
        
        self.add_log("⚙️ Настройки сохранены")
        messagebox.showinfo("Успех", "Настройки сохранены")
    
    def load_config(self):
        """Загрузка конфигурации"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    # Загружаем настройки
                    if 'voice_speed' in config:
                        self.speed_scale.set(config['voice_speed'])
                    
                    if 'volume' in config:
                        self.volume_scale.set(config['volume'])
                    
                    if 'auto_start' in config:
                        self.auto_start_var.set(config['auto_start'])
                    
                    if 'voice_activation' in config:
                        self.voice_activation_var.set(config['voice_activation'])
                    
                    self.add_log("⚙️ Конфигурация загружена")
        except Exception as e:
            self.add_log(f"❌ Ошибка загрузки конфигурации: {e}")
    
    def save_config(self):
        """Сохранение конфигурации"""
        config = {
            'user_name': self.assistant.user_name,
            'voice_speed': self.speed_scale.get(),
            'volume': self.volume_scale.get(),
            'auto_start': self.auto_start_var.get(),
            'voice_activation': self.voice_activation_var.get(),
            'weather_api_key': self.assistant.weather_api_key
        }
        
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.add_log("💾 Конфигурация сохранена")
        except Exception as e:
            self.add_log(f"❌ Ошибка сохранения конфигурации: {e}")
    
    def update_gui(self, event_type, data):
        """Обновление GUI на основе событий от помощника"""
        def update():
            if event_type == 'listening_start':
                self.update_indicator('listening')
                self.add_log("🎤 Начало прослушивания...")
                self.status_var.set("Слушаю...")
                
            elif event_type == 'processing_start':
                self.update_indicator('processing')
                self.add_log("🔍 Обработка команды...")
                self.status_var.set("Обрабатываю...")
                
            elif event_type == 'text_recognized':
                self.add_log(f"📝 Распознано: {data}")
                
            elif event_type == 'assistant_speak':
                self.add_log(f"🤖 Ответ: {data}")
                self.status_var.set("Говорю...")
                
            elif event_type == 'command_found':
                self.add_log(f"🎯 Выполняется команда: {data}")
                
            elif event_type == 'activated':
                self.update_indicator('on')
                self.add_log("🚀 Помощник активирован")
                self.status_var.set("Активирован")
                
            elif event_type == 'assistant_off':
                self.update_indicator('off')
                self.add_log("⏸️ Помощник выключен")
                self.status_var.set("Остановлен")
                
            elif event_type == 'error':
                self.add_log(f"❌ Ошибка: {data}")
                self.status_var.set("Ошибка")
                
            elif event_type == 'waiting_activation':
                self.status_var.set("Ожидание активации...")
                
            elif event_type == 'waiting_command':
                self.status_var.set("Ожидание команды...")
                
            elif event_type == 'timeout':
                self.add_log("⏰ Таймаут: голос не обнаружен")
                
            elif event_type == 'no_speech':
                self.add_log("❌ Речь не распознана")
                
            elif event_type == 'command_not_recognized':
                self.add_log(f"⚠️ Команда не распознана: {data}")
                
            # Обновляем статус
            self.status_var.set("Работаю..." if self.is_running else "Остановлен")
        
        # Обновляем GUI в основном потоке
        self.root.after(0, update)

def main():
    """Основная функция запуска GUI"""
    root = tk.Tk()
    app = VoxPersonalGUI(root)
    
    # Обработка закрытия окна
    def on_closing():
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            app.stop_assistant()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()