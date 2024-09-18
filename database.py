import sqlite3
import tkinter.messagebox as messagebox


def create_db():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT,
            description TEXT,
            receipt TEXT
        )
    ''')

    # Create income table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            source TEXT,
            date TEXT,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_expense(amount, category, date, description, receipt):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, date, description, receipt)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, category, date, description, receipt))
    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def add_income(amount, source, date, description):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO income (amount, source, date, description)
        VALUES (?, ?, ?, ?)
    ''', (amount, source, date, description))
    conn.commit()
    conn.close()

def view_income():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM income')
    income_data = cursor.fetchall()
    conn.close()
    return income_data

def delete_expense(expense_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

def delete_all_expenses():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses')
    conn.commit()
    conn.close()
