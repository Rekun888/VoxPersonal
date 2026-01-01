"""
VoxPersonal v6 - Premium AI Assistant Interface
Современный минималистичный интерфейс с неоновыми эффектами
"""

import tkinter as tk
from tkinter import ttk
import webbrowser

class VoxPersonalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VOX PERSONAL v6")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0a0a0a")
        
        # Ультра-современная цветовая схема
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_card': '#121212',
            'sidebar': '#1a1a1a',
            'primary': '#00ff88',  # Неоново-зеленый
            'secondary': '#0088ff',  # Неоново-синий
            'accent': '#ff0088',  # Неоново-розовый
            'text_primary': '#ffffff',
            'text_secondary': '#aaaaaa',
            'border': '#333333',
            'transparent': '#1a1a1a'
        }
        
        # Версии
        self.app_version = "v0.1"
        self.assistant_version = "V6"
        
        # Текущий активный раздел
        self.active_section = 'home'
        self.active_settings_subsection = 'general'
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_interface()
        
        # Центрирование окна
        self.center_window()
        
    def setup_styles(self):
        """Настройка современных шрифтов"""
        self.title_font = ('Segoe UI', 32, 'bold')
        self.header_font = ('Segoe UI', 18, 'bold')
        self.nav_font = ('Segoe UI', 12)
        self.body_font = ('Segoe UI', 11)
        self.button_font = ('Segoe UI', 10, 'bold')
        self.subnav_font = ('Segoe UI', 10)
        self.version_font = ('Segoe UI', 24, 'bold')
        self.developer_font = ('Segoe UI', 16, 'bold')
        self.info_font = ('Segoe UI', 14)
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_interface(self):
        """Создание ультра-современного интерфейса"""
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Боковая панель - Glassmorphism эффект
        self.create_sidebar(main_container)
        
        # Основное содержимое
        self.content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем страницы
        self.pages = {}
        self.create_home_page()
        self.create_account_page()
        self.create_settings_page()
        
        # Показываем главную страницу
        self.show_page('home')
    
    def create_sidebar(self, parent):
        """Создание стильной боковой панели"""
        sidebar = tk.Frame(parent, width=240, bg=self.colors['sidebar'])
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Логотип с неоновым эффектом
        logo_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        logo_frame.pack(pady=40)
        
        # Неоновый текст
        logo_label = tk.Label(logo_frame,
                            text="VOX\nPERSONAL",
                            font=('Segoe UI', 20, 'bold'),
                            bg=self.colors['sidebar'],
                            fg=self.colors['primary'],
                            justify=tk.CENTER)
        logo_label.pack()
        
        # Версия с glow эффектом
        version_label = tk.Label(logo_frame,
                               text="v6.0 | AI ASSISTANT",
                               font=('Segoe UI', 9),
                               bg=self.colors['sidebar'],
                               fg=self.colors['text_secondary'])
        version_label.pack(pady=5)
        
        # Горизонтальная линия с градиентом
        separator = tk.Frame(sidebar, height=1, bg='#333333')
        separator.pack(fill=tk.X, padx=20, pady=30)
        
        # Кнопки навигации с hover эффектами
        self.nav_buttons = {}
        nav_items = [
            ("🏠 ГЛАВНАЯ", "home", self.colors['primary']),
            ("👤 ПРОФИЛЬ", "account", self.colors['secondary']),
            ("⚙️ НАСТРОЙКИ", "settings", self.colors['accent'])
        ]
        
        for text, command, color in nav_items:
            btn_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
            btn_frame.pack(fill=tk.X, padx=0, pady=5)
            
            # Контейнер для кнопки и индикатора
            btn_container = tk.Frame(btn_frame, bg=self.colors['sidebar'])
            btn_container.pack(fill=tk.X, padx=10)
            
            # Индикатор активного раздела (слева)
            indicator = tk.Frame(btn_container, width=4, bg=self.colors['sidebar'])
            indicator.pack(side=tk.LEFT, fill=tk.Y)
            indicator.pack_propagate(False)
            
            # Сама кнопка
            btn = tk.Button(btn_container,
                          text=text,
                          font=self.nav_font,
                          bg=self.colors['sidebar'],
                          fg=self.colors['text_secondary'],
                          bd=0,
                          padx=15,
                          pady=15,
                          anchor='w',
                          activebackground='#222222',
                          activeforeground=color,
                          relief=tk.FLAT,
                          command=lambda cmd=command: self.show_page(cmd))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Сохраняем данные кнопки
            self.nav_buttons[command] = {
                'button': btn,
                'indicator': indicator,
                'color': color,
                'frame': btn_frame
            }
        
        # Изначально подсвечиваем главную
        self.update_nav_highlight()
        
        # Нижняя панель с информацией
        bottom_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        # Статус системы
        status_frame = tk.Frame(bottom_frame, bg=self.colors['sidebar'])
        status_frame.pack(pady=10)
        
        # Индикатор статуса
        self.status_indicator = tk.Canvas(status_frame, width=12, height=12, bg=self.colors['sidebar'], highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=(20, 10))
        self.status_indicator.create_oval(2, 2, 10, 10, fill=self.colors['primary'], outline='')
        
        tk.Label(status_frame,
                text="СИСТЕМА АКТИВНА",
                font=('Segoe UI', 9),
                bg=self.colors['sidebar'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        # Разработчик
        tk.Label(bottom_frame,
                text="Разработано Rekun888",
                font=('Segoe UI', 8),
                bg=self.colors['sidebar'],
                fg='#666666').pack(pady=5)
    
    def create_home_page(self):
        """Создание главной страницы"""
        page = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        self.pages['home'] = page
        
        # Карточка контента
        content_card = tk.Frame(page, bg=self.colors['bg_card'])
        content_card.pack(expand=True, padx=50, pady=50)
        
        # Заголовок страницы с неоновым эффектом
        title_label = tk.Label(content_card,
                             text="🏠 ГЛАВНАЯ",
                             font=self.title_font,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        title_label.pack(pady=40)
        
        # Субтитр
        subtitle_label = tk.Label(content_card,
                                text="Центр управления голосовым ассистентом",
                                font=self.body_font,
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=10)
        
        # Анимация загрузки
        loading_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        loading_frame.pack(pady=40)
        
        # Точки загрузки
        self.home_dots = []
        for i in range(3):
            dot = tk.Canvas(loading_frame, width=10, height=10, bg=self.colors['bg_card'], highlightthickness=0)
            dot.pack(side=tk.LEFT, padx=5)
            dot.create_oval(0, 0, 10, 10, fill=self.colors['primary'], outline='')
            self.home_dots.append(dot)
        
        # Сообщение
        message_label = tk.Label(content_card,
                               text="РАЗДЕЛ В РАЗРАБОТКЕ",
                               font=('Segoe UI', 14),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_secondary'])
        message_label.pack(pady=20)
        
        # Кнопка "Новости разработки" с неоновым эффектом
        self.create_news_button(content_card)
    
    def create_account_page(self):
        """Создание страницы профиля"""
        page = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        self.pages['account'] = page
        
        # Карточка контента
        content_card = tk.Frame(page, bg=self.colors['bg_card'])
        content_card.pack(expand=True, padx=50, pady=50)
        
        # Заголовок страницы с неоновым эффектом
        title_label = tk.Label(content_card,
                             text="👤 ПРОФИЛЬ",
                             font=self.title_font,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        title_label.pack(pady=40)
        
        # Субтитр
        subtitle_label = tk.Label(content_card,
                                text="Управление профилем и настройками пользователя",
                                font=self.body_font,
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=10)
        
        # Анимация загрузки
        loading_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        loading_frame.pack(pady=40)
        
        # Точки загрузки
        self.account_dots = []
        for i in range(3):
            dot = tk.Canvas(loading_frame, width=10, height=10, bg=self.colors['bg_card'], highlightthickness=0)
            dot.pack(side=tk.LEFT, padx=5)
            dot.create_oval(0, 0, 10, 10, fill=self.colors['secondary'], outline='')
            self.account_dots.append(dot)
        
        # Сообщение
        message_label = tk.Label(content_card,
                               text="РАЗДЕЛ В РАЗРАБОТКЕ",
                               font=('Segoe UI', 14),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_secondary'])
        message_label.pack(pady=20)
        
        # Кнопка "Новости разработки" с неоновым эффектом
        self.create_news_button(content_card)
    
    def create_settings_page(self):
        """Создание страницы настроек с подразделами"""
        page = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        self.pages['settings'] = page
        
        # Контейнер для двух колонок
        container = tk.Frame(page, bg=self.colors['bg_dark'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая колонка - подменю настроек
        left_column = tk.Frame(container, width=200, bg=self.colors['bg_dark'])
        left_column.pack(side=tk.LEFT, fill=tk.Y)
        left_column.pack_propagate(False)
        
        # Правая колонка - контент подраздела
        right_column = tk.Frame(container, bg=self.colors['bg_dark'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Создаем подменю настроек
        self.create_settings_submenu(left_column)
        
        # Создаем контейнер для подразделов с прокруткой
        self.create_scrollable_settings_content(right_column)
        
        # Создаем подразделы настроек
        self.settings_pages = {}
        self.create_general_settings()
        self.create_appearance_settings()
        self.create_launch_settings()
        self.create_about_settings()
        
        # Показываем первый подраздел
        self.show_settings_subsection('general')
    
    def create_settings_submenu(self, parent):
        """Создание подменю настроек"""
        # Заголовок подменю
        menu_header = tk.Label(parent,
                             text="НАСТРОЙКИ",
                             font=self.header_font,
                             bg=self.colors['bg_dark'],
                             fg=self.colors['text_primary'])
        menu_header.pack(anchor='w', pady=(0, 20))
        
        # Подразделы настроек
        self.settings_buttons = {}
        subsections = [
            ("⚙️ Основные", "general", self.colors['primary']),
            ("🎨 Оформление", "appearance", self.colors['secondary']),
            ("🚀 Параметры запуска", "launch", self.colors['accent']),
            ("ℹ️ О программе", "about", self.colors['text_secondary'])
        ]
        
        for text, command, color in subsections:
            btn_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
            btn_frame.pack(fill=tk.X, pady=3)
            
            # Индикатор активного подраздела
            indicator = tk.Frame(btn_frame, width=3, bg=self.colors['bg_dark'])
            indicator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
            indicator.pack_propagate(False)
            
            # Кнопка подраздела
            btn = tk.Button(btn_frame,
                          text=text,
                          font=self.subnav_font,
                          bg=self.colors['bg_dark'],
                          fg=self.colors['text_secondary'],
                          bd=0,
                          padx=10,
                          pady=12,
                          anchor='w',
                          activebackground='#222222',
                          activeforeground=color,
                          relief=tk.FLAT,
                          command=lambda cmd=command: self.show_settings_subsection(cmd))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Сохраняем кнопку
            self.settings_buttons[command] = {
                'button': btn,
                'indicator': indicator,
                'color': color,
                'frame': btn_frame
            }
        
        # Обновляем подсветку
        self.update_settings_highlight()
    
    def create_scrollable_settings_content(self, parent):
        """Создание прокручиваемого контейнера для подразделов настроек"""
        # Создаем canvas и скроллбар
        canvas = tk.Canvas(parent, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        # Настраиваем скроллбар
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Упаковываем элементы
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Добавляем прокрутку колесиком мыши
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Сохраняем ссылки
        self.settings_canvas = canvas
        self.settings_scrollable_frame = scrollable_frame
    
    def create_general_settings(self):
        """Создание раздела Основные настройки"""
        page = tk.Frame(self.settings_scrollable_frame, bg=self.colors['bg_dark'])
        self.settings_pages['general'] = page
        
        # Карточка контента
        content_card = tk.Frame(page, bg=self.colors['bg_card'])
        content_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок подраздела
        title_label = tk.Label(content_card,
                             text="⚙️ ОСНОВНЫЕ НАСТРОЙКИ",
                             font=self.header_font,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        title_label.pack(pady=30)
        
        # Описание подраздела
        desc_label = tk.Label(content_card,
                            text="Основные параметры и конфигурация системы",
                            font=self.body_font,
                            bg=self.colors['bg_card'],
                            fg=self.colors['text_secondary'])
        desc_label.pack(pady=10)
        
        # Анимация загрузки
        loading_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        loading_frame.pack(pady=30)
        
        # Точки загрузки
        dots = []
        for i in range(3):
            dot = tk.Canvas(loading_frame, width=8, height=8, bg=self.colors['bg_card'], highlightthickness=0)
            dot.pack(side=tk.LEFT, padx=3)
            dot.create_oval(0, 0, 8, 8, fill=self.colors['accent'], outline='')
            dots.append(dot)
        
        # Сообщение
        message_label = tk.Label(content_card,
                               text="ПОДРАЗДЕЛ В РАЗРАБОТКЕ",
                               font=('Segoe UI', 12),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_secondary'])
        message_label.pack(pady=20)
        
        # Кнопка "Новости разработки"
        self.create_news_button(content_card)
        
        # Добавляем высоту для прокрутки
        spacer = tk.Frame(content_card, height=400, bg=self.colors['bg_card'])
        spacer.pack(fill=tk.X, pady=20)
    
    def create_appearance_settings(self):
        """Создание раздела Оформление"""
        page = tk.Frame(self.settings_scrollable_frame, bg=self.colors['bg_dark'])
        self.settings_pages['appearance'] = page
        
        # Карточка контента
        content_card = tk.Frame(page, bg=self.colors['bg_card'])
        content_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок подраздела
        title_label = tk.Label(content_card,
                             text="🎨 ОФОРМЛЕНИЕ",
                             font=self.header_font,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        title_label.pack(pady=30)
        
        # Описание подраздела
        desc_label = tk.Label(content_card,
                            text="Настройки интерфейса и внешнего вида",
                            font=self.body_font,
                            bg=self.colors['bg_card'],
                            fg=self.colors['text_secondary'])
        desc_label.pack(pady=10)
        
        # Анимация загрузки
        loading_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        loading_frame.pack(pady=30)
        
        # Точки загрузки
        dots = []
        for i in range(3):
            dot = tk.Canvas(loading_frame, width=8, height=8, bg=self.colors['bg_card'], highlightthickness=0)
            dot.pack(side=tk.LEFT, padx=3)
            dot.create_oval(0, 0, 8, 8, fill=self.colors['accent'], outline='')
            dots.append(dot)
        
        # Сообщение
        message_label = tk.Label(content_card,
                               text="ПОДРАЗДЕЛ В РАЗРАБОТКЕ",
                               font=('Segoe UI', 12),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_secondary'])
        message_label.pack(pady=20)
        
        # Кнопка "Новости разработки"
        self.create_news_button(content_card)
        
        # Добавляем высоту для прокрутки
        spacer = tk.Frame(content_card, height=400, bg=self.colors['bg_card'])
        spacer.pack(fill=tk.X, pady=20)
    
    def create_launch_settings(self):
        """Создание раздела Параметры запуска"""
        page = tk.Frame(self.settings_scrollable_frame, bg=self.colors['bg_dark'])
        self.settings_pages['launch'] = page
        
        # Карточка контента
        content_card = tk.Frame(page, bg=self.colors['bg_card'])
        content_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок подраздела
        title_label = tk.Label(content_card,
                             text="🚀 ПАРАМЕТРЫ ЗАПУСКА",
                             font=self.header_font,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        title_label.pack(pady=30)
        
        # Описание подраздела
        desc_label = tk.Label(content_card,
                            text="Параметры автозапуска и инициализации",
                            font=self.body_font,
                            bg=self.colors['bg_card'],
                            fg=self.colors['text_secondary'])
        desc_label.pack(pady=10)
        
        # Анимация загрузки
        loading_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        loading_frame.pack(pady=30)
        
        # Точки загрузки
        dots = []
        for i in range(3):
            dot = tk.Canvas(loading_frame, width=8, height=8, bg=self.colors['bg_card'], highlightthickness=0)
            dot.pack(side=tk.LEFT, padx=3)
            dot.create_oval(0, 0, 8, 8, fill=self.colors['accent'], outline='')
            dots.append(dot)
        
        # Сообщение
        message_label = tk.Label(content_card,
                               text="ПОДРАЗДЕЛ В РАЗРАБОТКЕ",
                               font=('Segoe UI', 12),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_secondary'])
        message_label.pack(pady=20)
        
        # Кнопка "Новости разработки"
        self.create_news_button(content_card)
        
        # Добавляем высоту для прокрутки
        spacer = tk.Frame(content_card, height=400, bg=self.colors['bg_card'])
        spacer.pack(fill=tk.X, pady=20)
    
    def create_about_settings(self):
        """Создание раздела О программе с версиями"""
        page = tk.Frame(self.settings_scrollable_frame, bg=self.colors['bg_dark'])
        self.settings_pages['about'] = page
        
        # Карточка контента (занимает всю высоту)
        content_card = tk.Frame(page, bg=self.colors['bg_card'])
        content_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Контейнер для центрирования контента по вертикали
        center_container = tk.Frame(content_card, bg=self.colors['bg_card'])
        center_container.pack(expand=True, fill=tk.BOTH)
        
        # Верхняя часть (пустое пространство)
        top_spacer = tk.Frame(center_container, bg=self.colors['bg_card'], height=100)
        top_spacer.pack(fill=tk.X)
        
        # Заголовок подраздела
        title_label = tk.Label(center_container,
                             text="ℹ️ О ПРОГРАММЕ",
                             font=self.header_font,
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        title_label.pack(pady=20)
        
        # Описание подраздела
        desc_label = tk.Label(center_container,
                            text="Информация о программе и разработчике",
                            font=self.info_font,
                            bg=self.colors['bg_card'],
                            fg=self.colors['text_secondary'])
        desc_label.pack(pady=10)
        
        # Разделитель
        separator = tk.Frame(center_container, height=2, bg='#333333')
        separator.pack(fill=tk.X, pady=40)
        
        # Большая зона для версий
        version_container = tk.Frame(center_container, bg=self.colors['bg_card'])
        version_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Версия приложения (большая)
        app_version_frame = tk.Frame(version_container, bg=self.colors['bg_card'])
        app_version_frame.pack(pady=30)
        
        tk.Label(app_version_frame,
                text="Версия приложения",
                font=self.body_font,
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack()
        
        tk.Label(app_version_frame,
                text=self.app_version,
                font=self.version_font,
                bg=self.colors['bg_card'],
                fg=self.colors['primary']).pack(pady=10)
        
        # Версия ассистента (большая)
        assistant_version_frame = tk.Frame(version_container, bg=self.colors['bg_card'])
        assistant_version_frame.pack(pady=30)
        
        tk.Label(assistant_version_frame,
                text="Версия ассистента",
                font=self.body_font,
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack()
        
        tk.Label(assistant_version_frame,
                text=self.assistant_version,
                font=self.version_font,
                bg=self.colors['bg_card'],
                fg=self.colors['secondary']).pack(pady=10)
        
        # Разделитель
        separator2 = tk.Frame(center_container, height=2, bg='#333333')
        separator2.pack(fill=tk.X, pady=40)
        
        # Кнопка "Новости разработки"
        self.create_news_button(center_container)
        
        # Разделитель
        separator3 = tk.Frame(center_container, height=2, bg='#333333')
        separator3.pack(fill=tk.X, pady=40)
        
        # Разработчик
        developer_frame = tk.Frame(center_container, bg=self.colors['bg_card'])
        developer_frame.pack(pady=20)
        
        tk.Label(developer_frame,
                text="Разработчик",
                font=self.body_font,
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack()
        
        tk.Label(developer_frame,
                text="Rekun888",
                font=self.developer_font,
                bg=self.colors['bg_card'],
                fg=self.colors['accent']).pack(pady=10)
        
        # Дополнительная информация
        info_label = tk.Label(center_container,
                            text="VOX PERSONAL - Умный голосовой ассистент",
                            font=('Segoe UI', 11),
                            bg=self.colors['bg_card'],
                            fg='#666666')
        info_label.pack(pady=10)
        
        # Нижняя часть (пустое пространство)
        bottom_spacer = tk.Frame(center_container, bg=self.colors['bg_card'], height=100)
        bottom_spacer.pack(fill=tk.X)
        
        # Добавляем высоту для прокрутки
        spacer = tk.Frame(page, height=400, bg=self.colors['bg_dark'])
        spacer.pack(fill=tk.X, pady=20)
    
    def create_news_button(self, parent):
        """Создание стильной кнопки Новости разработки"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        btn_frame.pack(pady=20)
        
        # Основная кнопка
        news_btn = tk.Button(btn_frame,
                           text="📢 НОВОСТИ РАЗРАБОТКИ",
                           font=self.button_font,
                           bg=self.colors['bg_card'],
                           fg=self.colors['primary'],
                           bd=2,
                           relief=tk.FLAT,
                           padx=25,
                           pady=12,
                           cursor='hand2',
                           activebackground=self.colors['bg_card'],
                           activeforeground=self.colors['primary'],
                           command=self.open_github)
        news_btn.pack()
        
        # Добавляем hover эффект
        news_btn.bind("<Enter>", lambda e: news_btn.config(
            bg=self.colors['primary'], 
            fg=self.colors['bg_card'],
            bd=0
        ))
        news_btn.bind("<Leave>", lambda e: news_btn.config(
            bg=self.colors['bg_card'], 
            fg=self.colors['primary'],
            bd=2
        ))
        
        # Подсказка
        hint_label = tk.Label(parent,
                            text="Следите за обновлениями в GitHub репозитории",
                            font=('Segoe UI', 9),
                            bg=self.colors['bg_card'],
                            fg='#666666')
        hint_label.pack(pady=10)
    
    def animate_dots(self):
        """Анимация точек загрузки для всех страниц"""
        # Анимация точек на главной
        if hasattr(self, 'home_dots') and hasattr(self, 'home_dot_counter'):
            self.home_dot_counter = (self.home_dot_counter + 1) % 3
            for i, dot in enumerate(self.home_dots):
                if i == self.home_dot_counter:
                    dot.itemconfig(1, fill=self.colors['primary'])
                else:
                    dot.itemconfig(1, fill=self.colors['text_secondary'])
        else:
            self.home_dot_counter = 0
        
        # Анимация точек в профиле
        if hasattr(self, 'account_dots') and hasattr(self, 'account_dot_counter'):
            self.account_dot_counter = (self.account_dot_counter + 1) % 3
            for i, dot in enumerate(self.account_dots):
                if i == self.account_dot_counter:
                    dot.itemconfig(1, fill=self.colors['secondary'])
                else:
                    dot.itemconfig(1, fill=self.colors['text_secondary'])
        else:
            self.account_dot_counter = 0
        
        # Повторяем каждые 500мс
        self.root.after(500, self.animate_dots)
    
    def show_page(self, page_name):
        """Показать выбранную страницу"""
        # Обновляем активный раздел
        self.active_section = page_name
        
        # Скрыть все страницы
        for page in self.pages.values():
            page.pack_forget()
        
        # Показываем выбранную страницу
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        
        # Обновить подсветку кнопок
        self.update_nav_highlight()
        
        # Запускаем анимацию если еще не запущена
        if not hasattr(self, 'animation_running'):
            self.animation_running = True
            self.animate_dots()
    
    def show_settings_subsection(self, subsection_name):
        """Показать выбранный подраздел настроек"""
        # Обновляем активный подраздел
        self.active_settings_subsection = subsection_name
        
        # Скрыть все подразделы
        for page in self.settings_pages.values():
            page.pack_forget()
        
        # Показываем выбранный подраздел
        self.settings_pages[subsection_name].pack(fill=tk.BOTH, expand=True)
        
        # Прокручиваем наверх
        if hasattr(self, 'settings_canvas'):
            self.settings_canvas.yview_moveto(0)
        
        # Обновить подсветку кнопок подразделов
        self.update_settings_highlight()
    
    def update_nav_highlight(self):
        """Обновить подсветку активной кнопки навигации"""
        for name, btn_data in self.nav_buttons.items():
            if name == self.active_section:
                # Активная кнопка
                btn_data['button'].config(
                    fg=btn_data['color'],
                    bg='#222222'
                )
                btn_data['indicator'].config(bg=btn_data['color'])
                btn_data['frame'].config(bg='#222222')
            else:
                # Неактивная кнопка
                btn_data['button'].config(
                    fg=self.colors['text_secondary'],
                    bg=self.colors['sidebar']
                )
                btn_data['indicator'].config(bg=self.colors['sidebar'])
                btn_data['frame'].config(bg=self.colors['sidebar'])
    
    def update_settings_highlight(self):
        """Обновить подсветку активного подраздела настроек"""
        for name, btn_data in self.settings_buttons.items():
            if name == self.active_settings_subsection:
                # Активный подраздел
                btn_data['button'].config(
                    fg=btn_data['color'],
                    bg='#222222'
                )
                btn_data['indicator'].config(bg=btn_data['color'])
                btn_data['frame'].config(bg='#222222')
            else:
                # Неактивный подраздел
                btn_data['button'].config(
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_dark']
                )
                btn_data['indicator'].config(bg=self.colors['bg_dark'])
                btn_data['frame'].config(bg=self.colors['bg_dark'])
    
    def open_github(self):
        """Открыть GitHub репозиторий"""
        webbrowser.open("https://github.com/Rekun888/VoxPersonal")

def main():
    """Запуск приложения"""
    root = tk.Tk()
    
    # Иконка приложения
    try:
        root.iconbitmap("icons/logo.ico")
    except:
        pass
    
    app = VoxPersonalApp(root)
    
    # Обработка закрытия
    def on_closing():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()