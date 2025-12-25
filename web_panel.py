"""
Минимальная веб-панель управления
Одна HTML страница с JavaScript
"""

from flask import Flask, render_template_string
import threading

app = Flask(__name__)

# HTML шаблон в строке (без отдельных файлов)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoxPersonal Super Lite</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .status {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.2em;
        }
        .status.online {
            color: #4CAF50;
        }
        .commands {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 30px;
        }
        .command-btn {
            background: #4b6cb7;
            border: none;
            color: white;
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        .command-btn:hover {
            background: #3a559f;
        }
        .logs {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 10px;
            height: 200px;
            overflow-y: auto;
            font-family: monospace;
            margin-top: 20px;
        }
        .log-entry {
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ VoxPersonal Super Lite</h1>
        
        <div class="status online">
            ✅ Ассистент активен
        </div>
        
        <h2>Быстрые команды:</h2>
        <div class="commands">
            <button class="command-btn" onclick="sendCommand('привет')">👋 Привет</button>
            <button class="command-btn" onclick="sendCommand('как дела')">😊 Как дела?</button>
            <button class="command-btn" onclick="sendCommand('открой браузер')">🌐 Открыть браузер</button>
            <button class="command-btn" onclick="sendCommand('открой панель управления')">⚙️ Панель управления</button>
        </div>
        
        <h2>Логи:</h2>
        <div class="logs" id="logs">
            <div class="log-entry">Готов к работе</div>
        </div>
    </div>
    
    <script>
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
                addLog(`Отправлено: ${command}`);
                addLog(`Ответ: ${data.message}`);
            })
            .catch(error => {
                addLog(`Ошибка: ${error}`);
            });
        }
        
        function addLog(message) {
            const logs = document.getElementById('logs');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            logs.appendChild(entry);
            logs.scrollTop = logs.scrollHeight;
        }
        
        // Автоматическое обновление статуса
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.querySelector('.status').textContent = 
                        `✅ ${data.status} | ${data.commands_count} команд`;
                });
        }, 5000);
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
    return {
        'status': 'Активен',
        'version': '1.0',
        'commands_count': 5
    }

@app.route('/api/command', methods=['POST'])
def command():
    """Обработка команды"""
    import json
    data = request.json
    command = data.get('command', '')
    
    # Простая логика ответов
    responses = {
        'привет': 'Привет! Чем могу помочь?',
        'как дела': 'Всё отлично!',
        'открой браузер': 'Открываю браузер...',
        'открой панель управления': 'Открываю панель управления...'
    }
    
    message = responses.get(command, 'Неизвестная команда')
    
    # Если нужно выполнить действие
    if command == 'открой браузер':
        import webbrowser
        webbrowser.open("https://google.com")
    elif command == 'открой панель управления':
        import os
        os.system("control")
    
    return {'success': True, 'message': message}

def run_web_server():
    """Запуск веб-сервера"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_web_server()