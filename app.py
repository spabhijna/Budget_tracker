import multiprocessing
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from flask import Flask, render_template, request, jsonify

# Set the start method for multiprocessing (important for macOS)
multiprocessing.set_start_method('spawn', force=True)

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()

    # Drop existing tables and create new ones
    cursor.execute("DROP TABLE IF EXISTS income")
    cursor.execute("DROP TABLE IF EXISTS expenses")
    cursor.execute("DROP TABLE IF EXISTS savings")

    cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        amount REAL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS savings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        goal REAL,
                        contribution REAL DEFAULT 0,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_income', methods=['POST'])
def add_income():
    amount = request.form.get('amount', type=float)
    if amount:
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO income (amount) VALUES (?)", (amount,))
        conn.commit()
        conn.close()
        return jsonify(status='success', message='Income added successfully!')
    return jsonify(status='error', message='Amount is required!')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form.get('category')
    amount = request.form.get('amount', type=float)
    if category and amount:
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))
        conn.commit()
        conn.close()
        return jsonify(status='success', message='Expense added successfully!')
    return jsonify(status='error', message='Category and Amount are required!')

@app.route('/set_savings', methods=['POST'])
def set_savings():
    goal = request.form.get('goal', type=float)
    if goal:
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO savings (goal) VALUES (?)", (goal,))
        conn.commit()
        conn.close()
        return jsonify(status='success', message='Savings goal set successfully!')
    return jsonify(status='error', message='Goal amount is required!')

@app.route('/get_data')
def get_data():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sum(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT sum(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0
    cursor.execute("SELECT goal, contribution FROM savings ORDER BY id DESC LIMIT 1")
    savings = cursor.fetchone()
    savings_goal = savings[0] if savings else 0
    savings_contribution = savings[1] if savings else 0
    conn.close()

    return jsonify(
        total_income=total_income,
        total_expenses=total_expenses,
        savings_goal=savings_goal,
        savings_contribution=savings_contribution
    )

@app.route('/reset_db')
def reset_db():
    init_db()  # Re-initialize the database (drop and recreate tables)
    return jsonify(status="success", message="Database reset successfully!")

@app.route('/plot_expenses')
def plot_expenses():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    categories = [item[0] for item in data]
    amounts = [item[1] for item in data]

    plt.figure(figsize=(10, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(categories)))
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Convert plot to PNG image and encode it in base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('plot.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

