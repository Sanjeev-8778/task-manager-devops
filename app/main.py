from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Helper function to get a new DB connection
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", 5432)
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create tasks table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            description TEXT NOT NULL
        );
    """)

    if request.method == 'POST':
        task_desc = request.form['description']
        cur.execute("INSERT INTO tasks (description) VALUES (%s);", (task_desc,))
        conn.commit()

    cur.execute("SELECT id, description FROM tasks;")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
git add app/main.py