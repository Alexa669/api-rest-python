from flask import Flask, request, jsonify
from database import get_db_connection

app = Flask(__name__)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    description = data['description']
    due_date = data['due_date']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (description, due_date) VALUES (?, ?)', (description, due_date))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': task_id, 'description': description, 'due_date': due_date}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(dict(task))

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    result = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    
    return '', 204

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    description = data['description']
    due_date = data['due_date']
    
    conn = get_db_connection()
    result = conn.execute('UPDATE tasks SET description = ?, due_date = ? WHERE id = ?', 
                          (description, due_date, task_id))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'id': task_id, 'description': description, 'due_date': due_date})
