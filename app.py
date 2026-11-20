from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("tasks.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                due_date TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium',
                status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)

@app.route("/")
def index():
    init_db()
    status = request.args.get("status", "All")
    with get_db() as db:
        if status in ("Pending", "Completed"):
            tasks = db.execute("SELECT * FROM tasks WHERE status=? ORDER BY due_date", (status,)).fetchall()
        else:
            tasks = db.execute("SELECT * FROM tasks ORDER BY due_date").fetchall()
    return render_template("index.html", tasks=tasks, selected=status)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    if not title or not subject:
        flash("Task title and subject are required.", "error")
        return redirect(url_for("index"))
    with get_db() as db:
        db.execute(
            "INSERT INTO tasks (title, subject, due_date, priority) VALUES (?, ?, ?, ?)",
            (title, subject, request.form.get("due_date") or None,
             request.form.get("priority", "Medium"))
        )
    flash("Task added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    with get_db() as db:
        db.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok"}, 200

init_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )