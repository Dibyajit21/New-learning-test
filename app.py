import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "tasks.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"
        )

@app.route("/tasks", methods=["GET"])
def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT id, title FROM tasks").fetchall()
    return jsonify([{"id": row[0], "title": row[1]} for row in rows])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (data["title"],))
        task_id = cursor.lastrowid
    return jsonify({"id": task_id, "title": data["title"]}), 201

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
