"""
Веб-панель управления VoxPersonal v2
"""

from flask import Flask, render_template_string, jsonify, request
import threading
import json
import os
import webbrowser
import pyautogui

app = Flask(__name__)

# Текущий статус
current_status = {
    'volume': 50,
    'is_active': True,
    'last_command': None
}

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoxPersonal v2</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.8em;
            background: linear-gradient(90deg, #fff, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            margin-bottom: 30px;
            opacity: 0.8;
            font-size: 1.1em;
        }
        .status-bar {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4CAF50;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .volume-control {
            display: flex;
            align-items: center;
            gap: 15px;
            background: rgba(0,0,0,0.15);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 25px;
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
        }
        .commands-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .command-btn {
            background: linear-gradient(135deg, #4b6cb7, #3a559f);
            border: none;
            color: white;
            padding: 18px 15px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            text-align: center;
        }
        .command-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #3a559f, #2a448f);
        }
        .command-btn:active {
            transform: translateY(-1px);
        }
        .command-btn i {
            font-size: 24px;
        }
        .voice-test {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
        }
        .mic-btn {
            background: #ff6b6b;
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            transition: background 0.3s;
        }
        .mic-btn:hover {
            background: #ff5252;
        }
        .mic-btn.recording {
            background: #ff3838;
            animation: recording-pulse 1s infinite;
        }
        @keyframes recording-pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 56, 56, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(255, 56, 56, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 56, 56, 0); }
        }
        .logs {
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 15px;
            height: 250px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
        }
        .log-entry {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
        }
        .log-time {
            opacity: 0.7;
            font-size: 0.9em;
            min-width: 70px;
        }
        .log-message {
            flex-grow: 1;
            margin-left: 15px;
        }
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            background: #4CAF50;
            color: white;
            transform: translateX(120%);
            transition: transform 0.3s;
            z-index: 1000;
        }
        .notification.show {
            transform: translateX(0);
        }
        .notification.error {
            background: #ff6b6b;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <h1><i class="fas fa-microphone-alt"></i> VoxPersonal v2</h1>
        <div class="subtitle">Улучшенное распознавание речи • 7 команд</div>
        
        <div class="status-bar">
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span id="status-text">Активен • Готов к работе</span>
            </div>
            <div id="connection-status">
                <i class="fas fa-volume-up"></i> 
                Громкость: <span id="current-volume">50</span>%
            </div>
        </div>
        
        <div class="volume-control">
            <i class="fas fa-volume-down"></i>
            <input type="range" min="0" max="100" value="50" class="volume-slider" id="volume-slider">
            <i class="fas fa-volume-up"></i>
            <button class="command-btn" onclick="adjustVolume('down')" style="padding: 10px 15px;">
                <i class="fas fa-volume-down"></i> Тише
            </button>
            <button class="command-btn" onclick="adjustVolume('up')" style="padding: 10px 15px;">
                <i class="fas fa-volume-up"></i> Громче
            </button>
        </div>
        
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
            <button class="command-btn" onclick="sendCommand('открой панель управления')">
                <i class="fas fa-cog"></i> Панель управления
            </button>
            <button class="command-btn" onclick="sendCommand('громче')">
                <i class="fas fa-volume-up"></i> Громче
            </button>
            <button class="command-btn" onclick="sendCommand('тише')">
                <i class="fas fa-volume-down"></i> Тише
            </button>
            <button class="command-btn" onclick="sendCommand('пока')">
                <i class="fas fa-sign-out-alt"></i> Пока
            </button>
        </div>
        
        <div class="voice-test">
            <h3><i class="fas fa-microphone"></i> Тест голосовых команд</h3>
            <p style="margin-bottom: 15px; opacity: 0.8;">
                Нажмите кнопку и скажите команду для проверки распознавания
            </p>
            <button class="mic-btn" id="mic-button" onclick="toggleRecording()">
                <i class="fas fa-microphone"></i> Нажмите и говорите
            </button>
            <div id="voice-result" style="margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.2); 
                 border-radius: 8px; min-height: 40px; display: none;">
                <strong>Распознано:</strong> <span id="recognized-text"></span>
            </div>
        </div>
        
        <h3><i class="fas fa-history"></i> Журнал действий</h3>
        <div class="logs" id="logs">
            <div class="log-entry">
                <span class="log-time">00:00:00</span>
                <span class="log-message">Система запущена</span>
            </div>
        </div>
    </div>
    
    <div id="notification" class="notification"></div>
    
    <script>
        let isRecording = false;
        let mediaRecorder = null;
        let audioChunks = [];
        
        // Элементы DOM
        const logsElement = document.getElementById('logs');
        const statusText = document.getElementById('status-text');
        const currentVolume = document.getElementById('current-volume');
        const volumeSlider = document.getElementById('volume-slider');
        const micButton = document.getElementById('mic-button');
        const voiceResult = document.getElementById('voice-result');
        const recognizedText = document.getElementById('recognized-text');
        const notification = document.getElementById('notification');
        
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
                
                if (data.volume !== undefined) {
                    currentVolume.textContent = data.volume;
                    volumeSlider.value = data.volume;
                }
                
                showNotification(data.message, data.success ? 'success' : 'error');
            })
            .catch(error => {
                addLog(`Ошибка: ${error}`, 'error');
                showNotification('Ошибка соединения', 'error');
            });
        }
        
        // Регулировка громкости
        function adjustVolume(direction) {
            const command = direction === 'up' ? 'громче' : 'тише';
            sendCommand(command);
        }
        
        // Обновление слайдера громкости
        volumeSlider.addEventListener('input', function() {
            currentVolume.textContent = this.value;
            // Здесь можно добавить API вызов для установки точной громкости
        });
        
        // Запись голоса
        async function toggleRecording() {
            if (!isRecording) {
                // Начало записи
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
                    
                    voiceResult.style.display = 'block';
                    recognizedText.textContent = 'Запись...';
                    
                    addLog('Начата запись голоса', 'info');
                    
                } catch (error) {
                    addLog(`Ошибка доступа к микрофону: ${error}`, 'error');
                    showNotification('Нет доступа к микрофону', 'error');
                }
            } else {
                // Остановка записи
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                    isRecording = false;
                    micButton.classList.remove('recording');
                    micButton.innerHTML = '<i class="fas fa-microphone"></i> Нажмите и говорите';
                    
                    recognizedText.textContent = 'Обработка...';
                    addLog('Запись остановлена', 'info');
                }
            }
        }
        
        // Отправка аудио на сервер для распознавания
        async function sendAudioToServer(audioBlob) {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            
            try {
                const response = await fetch('/api/recognize', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success && data.text) {
                    recognizedText.textContent = data.text;
                    addLog(`Распознано: ${data.text}`, 'voice');
                    
                    // Автоматически выполняем команду если она распознана
                    if (data.is_command) {
                        sendCommand(data.text);
                    }
                } else {
                    recognizedText.textContent = 'Не удалось распознать речь';
                    addLog('Ошибка распознавания', 'error');
                }
            } catch (error) {
                recognizedText.textContent = 'Ошибка сервера';
                addLog(`Ошибка отправки аудио: ${error}`, 'error');
            }
        }
        
        // Добавление записи в журнал
        function addLog(message, type = 'info') {
            const logs = document.getElementById('logs');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            
            const time = new Date().toLocaleTimeString();
            const typeIcon = {
                'command': '🚀',
                'response': '🗣️',
                'voice': '🎤',
                'info': 'ℹ️',
                'error': '❌'
            }[type] || 'ℹ️';
            
            entry.innerHTML = `
                <span class="log-time">${time}</span>
                <span class="log-message">${typeIcon} ${message}</span>
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
        
        // Автоматическое обновление статуса
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    statusText.textContent = `${data.status} • ${data.commands_count} команд`;
                    currentVolume.textContent = data.volume;
                    volumeSlider.value = data.volume;
                })
                .catch(error => {
                    console.error('Ошибка обновления статуса:', error);
                });
        }
        
        // Обновление каждые 3 секунды
        setInterval(updateStatus, 3000);
        
        // Инициализация
        updateStatus();
        addLog('Веб-панель загружена', 'info');
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
    """Статус ассистента"""
    return jsonify({
        'status': 'Активен',
        'version': '2.0',
        'commands_count': 7,
        'volume': current_status['volume'],
        'last_command': current_status['last_command']
    })

@app.route('/api/command', methods=['POST'])
def command():
    """Обработка команды"""
    try:
        data = request.json
        command_text = data.get('command', '').lower()
        
        # Обновляем статус
        current_status['last_command'] = command_text
        
        # Определяем ответ
        responses = {
            'привет': 'Привет! Чем могу помочь?',
            'как дела': 'Всё отлично! Готов помогать.',
            'открой браузер': 'Открываю браузер с Google...',
            'открой панель управления': 'Открываю панель управления Windows...',
            'громче': 'Увеличиваю громкость...',
            'тише': 'Уменьшаю громкость...',
            'пока': 'Пока! Возвращайтесь скорее!'
        }
        
        message = responses.get(command_text, 'Неизвестная команда')
        success = command_text in responses
        
        # Выполняем действие
        if command_text == 'открой браузер':
            webbrowser.open("https://google.com")
        elif command_text == 'открой панель управления':
            import os
            if os.name == 'nt':
                os.system("control")
        elif command_text == 'громче':
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            current_status['volume'] = min(100, current_status['volume'] + 20)
        elif command_text == 'тише':
            pyautogui.press('volumedown')
            pyautogui.press('volumedown')
            current_status['volume'] = max(0, current_status['volume'] - 20)
        
        return jsonify({
            'success': success,
            'message': message,
            'command': command_text,
            'volume': current_status['volume']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}',
            'command': 'error'
        })

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """Распознавание речи из аудио"""
    try:
        # В реальной реализации здесь было бы распознавание через Google Speech API
        # Но для простоты вернем заглушку
        import random
        
        # Имитация распознавания
        commands = ['привет', 'как дела', 'открой браузер', 'громче', 'тише', 'пока']
        recognized = random.choice(commands + ['не удалось распознать'])
        
        is_command = recognized in commands
        
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