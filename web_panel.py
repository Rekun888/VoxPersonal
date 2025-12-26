"""
Веб-панель VoxPersonal v3 с управлением медиа
"""

from flask import Flask, render_template_string, jsonify, request
import threading
import webbrowser
import pyautogui
import psutil
import os

app = Flask(__name__)

# Состояние системы
system_state = {
    'volume': 50,
    'media_state': 'stopped',  # stopped, playing, paused
    'browser_open': False,
    'last_command': None
}

# HTML шаблон с управлением медиа
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoxPersonal v3 - Управление медиа</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        h1 {
            font-size: 2.8em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #fff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            opacity: 0.8;
            font-size: 1.1em;
        }
        .status-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .status-card {
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s;
        }
        .status-card:hover {
            transform: translateY(-3px);
        }
        .status-value {
            font-size: 1.8em;
            font-weight: bold;
            margin-top: 10px;
        }
        .status-card.volume { border-left: 4px solid #4b6cb7; }
        .status-card.media { border-left: 4px solid #ff6b6b; }
        .status-card.browser { border-left: 4px solid #00ff88; }
        
        .sections {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        .section {
            background: rgba(0,0,0,0.15);
            padding: 25px;
            border-radius: 15px;
        }
        .section h3 {
            margin-bottom: 20px;
            color: #00ff88;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Команды */
        .commands-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
        }
        .command-btn {
            background: linear-gradient(135deg, rgba(75, 108, 183, 0.8), rgba(58, 85, 159, 0.8));
            border: none;
            color: white;
            padding: 16px 10px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 500;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            text-align: center;
            backdrop-filter: blur(5px);
        }
        .command-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #4b6cb7, #3a559f);
        }
        .command-btn i { font-size: 22px; }
        
        /* Управление медиа */
        .media-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
        }
        .media-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .media-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: scale(1.1);
        }
        .media-btn.play { background: rgba(0, 255, 136, 0.3); }
        .media-btn.pause { background: rgba(255, 107, 107, 0.3); }
        .media-btn.stop { background: rgba(255, 193, 7, 0.3); }
        
        /* Громкость */
        .volume-control {
            margin-top: 20px;
        }
        .volume-slider-container {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 10px;
        }
        .volume-slider {
            flex-grow: 1;
            height: 8px;
            -webkit-appearance: none;
            background: rgba(255,255,255,0.2);
            border-radius: 4px;
            outline: none;
        }
        .volume-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #4b6cb7;
            cursor: pointer;
            border: 2px solid white;
        }
        
        /* Журнал */
        .logs {
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 15px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
        }
        .log-entry {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .log-time {
            opacity: 0.7;
            font-size: 0.9em;
            min-width: 70px;
        }
        .log-type {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }
        .log-type.command { background: #4b6cb7; }
        .log-type.response { background: #00ff88; }
        .log-type.media { background: #ff6b6b; }
        .log-type.system { background: #ffc107; }
        .log-message {
            flex-grow: 1;
        }
        
        /* Уведомления */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            background: #00ff88;
            color: #000;
            font-weight: bold;
            transform: translateX(120%);
            transition: transform 0.3s;
            z-index: 1000;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .notification.show {
            transform: translateX(0);
        }
        .notification.error {
            background: #ff6b6b;
            color: white;
        }
        
        /* Микрофон */
        .voice-control {
            margin-top: 20px;
            text-align: center;
        }
        .mic-btn {
            background: linear-gradient(135deg, #ff6b6b, #ff5252);
            border: none;
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s;
            box-shadow: 0 10px 20px rgba(255,107,107,0.3);
        }
        .mic-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 25px rgba(255,107,107,0.4);
        }
        .mic-btn.recording {
            animation: pulse 1.5s infinite;
            background: linear-gradient(135deg, #ff3838, #ff0000);
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 56, 56, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(255, 56, 56, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 56, 56, 0); }
        }
        
        /* Адаптивность */
        @media (max-width: 768px) {
            .container { padding: 20px; }
            .commands-grid { grid-template-columns: repeat(2, 1fr); }
            .sections { grid-template-columns: 1fr; }
            h1 { font-size: 2.2em; }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-microphone-alt"></i> VoxPersonal v3</h1>
            <div class="subtitle">Управление медиа • 10 команд • Улучшенное распознавание</div>
        </div>
        
        <div class="status-bar">
            <div class="status-card volume">
                <div><i class="fas fa-volume-up"></i> Громкость</div>
                <div class="status-value" id="current-volume">50%</div>
            </div>
            <div class="status-card media">
                <div><i class="fas fa-play-circle"></i> Медиа</div>
                <div class="status-value" id="media-state">Остановлено</div>
            </div>
            <div class="status-card browser">
                <div><i class="fas fa-globe"></i> Браузер</div>
                <div class="status-value" id="browser-status">Закрыт</div>
            </div>
        </div>
        
        <div class="sections">
            <!-- Основные команды -->
            <div class="section">
                <h3><i class="fas fa-commands"></i> Основные команды</h3>
                <div class="commands-grid">
                    <button class="command-btn" onclick="sendCommand('привет')">
                        <i class="fas fa-hand-wave"></i> Привет
                    </button>
                    <button class="command-btn" onclick="sendCommand('как дела')">
                        <i class="fas fa-smile"></i> Как дела?
                    </button>
                    <button class="command-btn" onclick="sendCommand('открой браузер')">
                        <i class="fas fa-globe"></i> Браузер
                    </button>
                    <button class="command-btn" onclick="sendCommand('закрой браузер')">
                        <i class="fas fa-times-circle"></i> Закрыть браузер
                    </button>
                    <button class="command-btn" onclick="sendCommand('открой панель управления')">
                        <i class="fas fa-cog"></i> Панель управления
                    </button>
                    <button class="command-btn" onclick="sendCommand('пока')">
                        <i class="fas fa-sign-out-alt"></i> Пока
                    </button>
                </div>
            </div>
            
            <!-- Управление медиа -->
            <div class="section">
                <h3><i class="fas fa-music"></i> Управление медиа</h3>
                
                <div class="media-controls">
                    <button class="media-btn play" onclick="sendCommand('пауза')" title="Пауза/Продолжить">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="media-btn pause" onclick="sendCommand('продолжи')" title="Продолжить">
                        <i class="fas fa-pause"></i>
                    </button>
                    <button class="media-btn stop" onclick="sendCommand('стоп')" title="Стоп">
                        <i class="fas fa-stop"></i>
                    </button>
                </div>
                
                <div class="volume-control">
                    <div style="margin: 15px 0 10px; display: flex; justify-content: space-between;">
                        <span><i class="fas fa-volume-down"></i> Громкость</span>
                        <span id="volume-text">50%</span>
                    </div>
                    <div class="volume-slider-container">
                        <button class="command-btn" onclick="sendCommand('тише')" style="padding: 10px 15px;">
                            <i class="fas fa-volume-down"></i>
                        </button>
                        <input type="range" min="0" max="100" value="50" class="volume-slider" id="volume-slider">
                        <button class="command-btn" onclick="sendCommand('громче')" style="padding: 10px 15px;">
                            <i class="fas fa-volume-up"></i>
                        </button>
                    </div>
                </div>
                
                <div class="voice-control">
                    <button class="mic-btn" id="mic-button" onclick="toggleRecording()">
                        <i class="fas fa-microphone"></i> Голосовая команда
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Журнал -->
        <div class="section">
            <h3><i class="fas fa-history"></i> Журнал действий</h3>
            <div class="logs" id="logs">
                <div class="log-entry">
                    <div class="log-time">00:00:00</div>
                    <div class="log-type system"><i class="fas fa-power-off"></i></div>
                    <div class="log-message">Система запущена</div>
                </div>
            </div>
        </div>
    </div>
    
    <div id="notification" class="notification"></div>
    
    <script>
        // Элементы DOM
        const logsElement = document.getElementById('logs');
        const volumeSlider = document.getElementById('volume-slider');
        const volumeText = document.getElementById('volume-text');
        const currentVolume = document.getElementById('current-volume');
        const mediaState = document.getElementById('media-state');
        const browserStatus = document.getElementById('browser-status');
        const notification = document.getElementById('notification');
        const micButton = document.getElementById('mic-button');
        
        let isRecording = false;
        let mediaRecorder = null;
        let audioChunks = [];
        
        // Отправка команды
        function sendCommand(command) {
            fetch('/api/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({command: command})
            })
            .then(response => response.json())
            .then(data => {
                addLog(`Команда: ${command}`, 'command');
                addLog(`Ответ: ${data.message}`, 'response');
                
                // Обновляем состояние
                if (data.volume !== undefined) {
                    updateVolume(data.volume);
                }
                if (data.media_state) {
                    updateMediaState(data.media_state);
                }
                if (data.browser_open !== undefined) {
                    updateBrowserStatus(data.browser_open);
                }
                
                showNotification(data.message, data.success ? 'success' : 'error');
            })
            .catch(error => {
                addLog(`Ошибка: ${error}`, 'error');
                showNotification('Ошибка соединения', 'error');
            });
        }
        
        // Управление громкостью
        function updateVolume(volume) {
            currentVolume.textContent = volume + '%';
            volumeText.textContent = volume + '%';
            volumeSlider.value = volume;
        }
        
        volumeSlider.addEventListener('input', function() {
            updateVolume(this.value);
        });
        
        // Обновление состояния медиа
        function updateMediaState(state) {
            const states = {
                'stopped': 'Остановлено',
                'playing': 'Воспроизводится',
                'paused': 'На паузе'
            };
            mediaState.textContent = states[state] || state;
        }
        
        // Обновление статуса браузера
        function updateBrowserStatus(isOpen) {
            browserStatus.textContent = isOpen ? 'Открыт' : 'Закрыт';
            browserStatus.style.color = isOpen ? '#00ff88' : '#ff6b6b';
        }
        
        // Запись голоса
        async function toggleRecording() {
            if (!isRecording) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];
                    
                    mediaRecorder.ondataavailable = event => {
                        audioChunks.push(event.data);
                    };
                    
                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        await sendAudioToServer(audioBlob);
                        stream.getTracks().forEach(track => track.stop());
                    };
                    
                    mediaRecorder.start();
                    isRecording = true;
                    micButton.classList.add('recording');
                    micButton.innerHTML = '<i class="fas fa-stop"></i> Остановить запись';
                    
                    addLog('Запись голоса начата', 'media');
                    
                } catch (error) {
                    addLog(`Ошибка микрофона: ${error}`, 'error');
                    showNotification('Нет доступа к микрофону', 'error');
                }
            } else {
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                    isRecording = false;
                    micButton.classList.remove('recording');
                    micButton.innerHTML = '<i class="fas fa-microphone"></i> Голосовая команда';
                    addLog('Запись остановлена', 'media');
                }
            }
        }
        
        // Отправка аудио на сервер
        async function sendAudioToServer(audioBlob) {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'voice_command.wav');
            
            try {
                const response = await fetch('/api/recognize', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success && data.text) {
                    addLog(`Распознано: ${data.text}`, 'media');
                    
                    // Автоматически выполняем команду
                    if (data.is_command) {
                        sendCommand(data.text);
                    }
                } else {
                    addLog('Не удалось распознать речь', 'error');
                }
            } catch (error) {
                addLog(`Ошибка отправки аудио: ${error}`, 'error');
            }
        }
        
        // Добавление записи в журнал
        function addLog(message, type = 'system') {
            const logs = document.getElementById('logs');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            
            const time = new Date().toLocaleTimeString();
            const typeIcons = {
                'command': 'fas fa-rocket',
                'response': 'fas fa-comment',
                'media': 'fas fa-music',
                'system': 'fas fa-info-circle',
                'error': 'fas fa-exclamation-circle'
            };
            
            const typeColors = {
                'command': '#4b6cb7',
                'response': '#00ff88',
                'media': '#ff6b6b',
                'system': '#ffc107',
                'error': '#ff5252'
            };
            
            entry.innerHTML = `
                <div class="log-time">${time}</div>
                <div class="log-type" style="background: ${typeColors[type] || '#ffc107'}">
                    <i class="${typeIcons[type] || 'fas fa-info-circle'}"></i>
                </div>
                <div class="log-message">${message}</div>
            `;
            
            logs.appendChild(entry);
            logs.scrollTop = logs.scrollHeight;
        }
        
        // Показать уведомление
        function showNotification(message, type = 'success') {
            notification.textContent = message;
            notification.className = `notification ${type} show`;
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        // Обновление состояния системы
        function updateSystemStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateVolume(data.volume);
                    updateMediaState(data.media_state);
                    updateBrowserStatus(data.browser_open);
                })
                .catch(error => {
                    console.error('Ошибка обновления статуса:', error);
                });
        }
        
        // Горячие клавиши
        document.addEventListener('keydown', (event) => {
            // Space - пауза/продолжить
            if (event.code === 'Space') {
                event.preventDefault();
                sendCommand('пауза');
            }
            // Escape - стоп
            if (event.code === 'Escape') {
                sendCommand('стоп');
            }
            // F2 - привет
            if (event.code === 'F2') {
                sendCommand('привет');
            }
        });
        
        // Автоматическое обновление
        setInterval(updateSystemStatus, 2000);
        
        // Инициализация
        updateSystemStatus();
        addLog('Веб-панель загружена', 'system');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Статус системы"""
    # Проверяем открыт ли браузер
    browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe']
    browser_open = False
    
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in browsers:
                browser_open = True
                break
        except:
            continue
    
    return jsonify({
        'status': 'active',
        'version': '3.0',
        'commands_count': 10,
        'volume': system_state['volume'],
        'media_state': system_state['media_state'],
        'browser_open': browser_open,
        'last_command': system_state['last_command']
    })

@app.route('/api/command', methods=['POST'])
def command():
    """Обработка команды"""
    try:
        data = request.json
        command_text = data.get('command', '').lower()
        
        # Обновляем состояние
        system_state['last_command'] = command_text
        
        # Определяем ответ и действие
        responses = {
            'привет': 'Привет! Рад вас слышать.',
            'как дела': 'Всё прекрасно! Готов помочь.',
            'открой браузер': 'Открываю браузер с Google...',
            'закрой браузер': 'Закрываю браузеры...',
            'открой панель управления': 'Открываю панель управления...',
            'громче': 'Увеличиваю громкость...',
            'тише': 'Уменьшаю громкость...',
            'стоп': 'Останавливаю воспроизведение...',
            'пауза': 'Ставлю на паузу...',
            'продолжи': 'Продолжаю воспроизведение...',
            'пока': 'До свидания! Возвращайтесь...'
        }
        
        message = responses.get(command_text, 'Неизвестная команда')
        success = command_text in responses
        
        # Выполняем действие
        if command_text == 'открой браузер':
            webbrowser.open("https://google.com")
            system_state['browser_open'] = True
            
        elif command_text == 'закрой браузер':
            browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe']
            closed = 0
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in browsers:
                        proc.kill()
                        closed += 1
                except:
                    continue
            
            system_state['browser_open'] = False
            message = f"Закрыто {closed} браузеров"
            
        elif command_text == 'открой панель управления':
            import os
            if os.name == 'nt':
                os.system("control")
                
        elif command_text == 'громче':
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            system_state['volume'] = min(100, system_state['volume'] + 20)
            
        elif command_text == 'тише':
            pyautogui.press('volumedown')
            pyautogui.press('volumedown')
            system_state['volume'] = max(0, system_state['volume'] - 20)
            
        elif command_text == 'стоп':
            pyautogui.press('stop')
            system_state['media_state'] = 'stopped'
            
        elif command_text in ['пауза', 'продолжи']:
            pyautogui.press('playpause')
            
            if system_state['media_state'] == 'playing':
                system_state['media_state'] = 'paused'
            else:
                system_state['media_state'] = 'playing'
        
        return jsonify({
            'success': success,
            'message': message,
            'command': command_text,
            'volume': system_state['volume'],
            'media_state': system_state['media_state'],
            'browser_open': system_state.get('browser_open', False)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        })

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """Распознавание речи (заглушка)"""
    try:
        import random
        
        # Команды для распознавания
        commands = [
            'привет', 'как дела', 'открой браузер', 'закрой браузер',
            'громче', 'тише', 'стоп', 'пауза', 'продолжи', 'пока'
        ]
        
        # С вероятностью 80% распознаем команду
        if random.random() < 0.8:
            recognized = random.choice(commands)
            is_command = True
        else:
            recognized = random.choice(['не понял', 'повторите', 'что вы сказали'])
            is_command = False
        
        return jsonify({
            'success': True,
            'text': recognized,
            'is_command': is_command
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'text': f'Ошибка: {str(e)}',
            'is_command': False
        })

def run_web_server():
    """Запуск веб-сервера"""
    print("🌐 Веб-панель запущена: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_web_server()