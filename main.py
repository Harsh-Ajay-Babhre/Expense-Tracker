import sqlite3
from database import create_db

def modify_expenses_table():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    # Check if the expenses table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses';")
    table_exists = cursor.fetchone()

    if table_exists:
        # Rename the existing table
        cursor.execute('ALTER TABLE expenses RENAME TO old_expenses')
        
        # Create the new table with the additional receipt column
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                date TEXT,
                description TEXT,
                receipt TEXT
            )
        ''')
        
        # Copy the data from the old table to the new table
        cursor.execute('''
            INSERT INTO expenses (id, amount, category, date, description)
            SELECT id, amount, category, date, description
            FROM old_expenses
        ''')
        
        # Drop the old table
        cursor.execute('DROP TABLE old_expenses')
        
        print("Table modified successfully.")
    else:
        print("Expenses table does not exist. Creating a new table...")
        create_db()  # Create the table if it doesn't exist

    conn.commit()
    conn.close()

modify_expenses_table()  # Run this function once to modify the table



#--------------------------------------------------------------------------------------------------------------------------------------------------#
from tkinter import filedialog
from database import create_db, add_expense, view_expenses, add_income, view_income, delete_expense

def main():
    create_db()  # Ensure the database is created when the script is run
    
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Add Income")
        print("4. View Income")
        print("5. Delete Expense")  
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("Adding expense...")  # Debugging print statement
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            print(f"Expense details: {amount}, {category}, {date}, {description}")  # Debugging print statement
            # Temporarily bypass file dialog for testing purposes
            receipt_path = ""  
            add_expense(amount, category, date, description, receipt_path)
            print("Expense added successfully.")  # Debugging print statement
        
        elif choice == '2':
            print("Viewing expenses...")
            view_expenses()
        
        elif choice == '3':
            print("Adding income...")
            amount = float(input("Enter amount: "))
            source = input("Enter source: ")
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            add_income(amount, source, date, description)
            print("Income added successfully.")  # Debugging print statement
        
        elif choice == '4':
            print("Viewing income...")
            view_income()
        
        elif choice == '5':
            print("Deleting expense...")  # Debugging print statement
            view_expenses()  # Show all expenses before deletion
            expense_id = int(input("Enter ID of the expense to delete: "))
            delete_expense(expense_id)  # Call the delete function using the id
            print("Expense deleted successfully.")  # Debugging print statement
        
        elif choice == '6':
            print("Exiting program...")  # Debugging print statement
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
