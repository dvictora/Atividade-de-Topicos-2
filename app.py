from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Lista para armazenar as tarefas (em memória)
tasks = []

# Template HTML
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciador de Tarefas - Docker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 12px 25px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #5568d3;
        }
        
        .task-list {
            list-style: none;
        }
        
        .task-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s;
        }
        
        .task-item:hover {
            transform: translateX(5px);
        }
        
        .task-content {
            flex: 1;
        }
        
        .task-name {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .task-time {
            font-size: 12px;
            color: #999;
        }
        
        .delete-btn {
            padding: 8px 15px;
            background: #e74c3c;
            font-size: 14px;
        }
        
        .delete-btn:hover {
            background: #c0392b;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        
        .stats {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
        }
        
        .docker-badge {
            display: inline-block;
            background: #2496ed;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Gerenciador de Tarefas</h1>
        <p class="subtitle">Aplicação Flask rodando em Docker</p>
        
        <div class="input-group">
            <input type="text" id="taskInput" placeholder="Digite uma nova tarefa..." onkeypress="if(event.key==='Enter') addTask()">
            <button onclick="addTask()">Adicionar</button>
        </div>
        
        <ul class="task-list" id="taskList"></ul>
        
        <div class="stats">
            <strong>Total de tarefas:</strong> <span id="taskCount">0</span>
            <div class="docker-badge">🐳 Running on Docker</div>
        </div>
    </div>
    
    <script>
        function loadTasks() {
            fetch('/api/tasks')
                .then(response => response.json())
                .then(data => {
                    const taskList = document.getElementById('taskList');
                    const taskCount = document.getElementById('taskCount');
                    
                    if (data.tasks.length === 0) {
                        taskList.innerHTML = '<div class="empty-state">Nenhuma tarefa cadastrada. Adicione uma acima!</div>';
                    } else {
                        taskList.innerHTML = data.tasks.map(task => `
                            <li class="task-item">
                                <div class="task-content">
                                    <div class="task-name">${task.name}</div>
                                    <div class="task-time">Criada em: ${task.created_at}</div>
                                </div>
                                <button class="delete-btn" onclick="deleteTask(${task.id})">Excluir</button>
                            </li>
                        `).join('');
                    }
                    
                    taskCount.textContent = data.tasks.length;
                });
        }
        
        function addTask() {
            const input = document.getElementById('taskInput');
            const taskName = input.value.trim();
            
            if (taskName === '') {
                alert('Por favor, digite uma tarefa!');
                return;
            }
            
            fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: taskName})
            })
            .then(response => response.json())
            .then(() => {
                input.value = '';
                loadTasks();
            });
        }
        
        function deleteTask(id) {
            fetch(`/api/tasks/${id}`, {method: 'DELETE'})
                .then(() => loadTasks());
        }
        
        // Carregar tarefas ao iniciar
        loadTasks();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {
        'id': len(tasks) + 1,
        'name': data['name'],
        'created_at': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 204

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'tasks_count': len(tasks)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)