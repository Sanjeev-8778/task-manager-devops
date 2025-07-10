from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        dbname=os.environ.get('DB_NAME', 'tasks_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        port=os.environ.get('DB_PORT', 5432)
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        task = request.form['task']
        cur.execute("INSERT INTO tasks (description) VALUES (%s)", (task,))
        conn.commit()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
