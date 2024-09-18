import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox, Text
from tkcalendar import Calendar
from database import add_expense, view_expenses, add_income, view_income, delete_expense, delete_all_expenses
import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd
import squarify 
from PIL import Image, ImageTk, ImageSequence
from customtkinter import CTkImage
from chatbot import process_command, get_highest_spending_category, analyze_category_spending, list_subcategories 

# Set the theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("800x700")  # Increased width for chatbot

# Global variables to store dataset information
expense_data = []
subcategory_details = defaultdict(list)

# Function to toggle between dark and light modes
def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    if current_mode is None or current_mode == "Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

# Header Label
header_label = ctk.CTkLabel(app, text="Financial.Intelligent.Network.Assistant", font=("Helvetica", 24, "bold"))
header_label.pack(pady=20)

# Add a dark/light mode toggle switch
mode_switch = ctk.CTkSwitch(app, text="Toggle Dark/Light Mode", command=toggle_mode)
mode_switch.pack(pady=10)

# Chatbot Frame
chatbot_frame = ctk.CTkFrame(app)
chatbot_frame.pack(pady=15, padx=20, fill="both", expand=True)

chat_display = Text(chatbot_frame, height=10, wrap="word", state="normal")
chat_display.pack(padx=5, pady=5, fill="both", expand=True)

chat_input = ctk.CTkEntry(chatbot_frame, width=300, placeholder_text="Type your command...")
chat_input.pack(side="left", padx=5, pady=5, fill="x", expand=True)

def add_chat_message(message, sender="User"):
    chat_display.configure(state="normal")
    chat_display.insert("end", f"{sender}: {message}\n")
    chat_display.configure(state="disabled")
    chat_display.yview("end")

def handle_chatbot_command(event=None):
    user_input = chat_input.get().strip().lower()
    if user_input:
        add_chat_message(user_input, sender="User")

        if user_input == "upload dataset":
            # Trigger the file upload
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
            if file_path:
                # Process the uploaded file
                if file_path.endswith('.csv'):
                    data = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    data = pd.read_excel(file_path)
                else:
                    add_chat_message("Unsupported file format.", sender="Bot")
                    return

                # Process the data to update `expense_data` and `subcategory_details`
                expense_data.clear()
                subcategory_details.clear()
                for index, row in data.iterrows():
                    expense_data.append((None, row['Amount'], row['Category'], row['Date'], row['Description']))
                    subcategory_details[row['Category']].append((row['Description'], row['Amount']))

                add_chat_message(f"Dataset loaded successfully from {file_path}.", sender="Bot")

        elif user_input == "generate chart":
            if expense_data:
                add_chat_message("Generating the treemap chart...", sender="Bot")
                # Call the function to generate the chart
                view_expense_treemap()
            else:
                add_chat_message("No data available. Please upload a dataset first.", sender="Bot")

        else:
            # Process other commands using the function in chatbot.py
            result = process_command(user_input, expense_data, chat_display, subcategory_details)
            add_chat_message(result, sender="Bot")

        chat_input.delete(0, "end")

chat_input.bind("<Return>", handle_chatbot_command)

# Function to handle adding expenses
def open_add_expense():
    expense_window = ctk.CTkToplevel(app)
    expense_window.title("Add Expense")
    expense_window.geometry("400x500")

    amount_label = ctk.CTkLabel(expense_window, text="Amount:", font=("Helvetica", 16))
    amount_label.pack(pady=5)
    amount_entry = ctk.CTkEntry(expense_window, width=300)
    amount_entry.pack(pady=5)

    category_label = ctk.CTkLabel(expense_window, text="Category:", font=("Helvetica", 16))
    category_label.pack(pady=5)
    category_entry = ctk.CTkEntry(expense_window, width=300)
    category_entry.pack(pady=5)

    date_label = ctk.CTkLabel(expense_window, text="Select Date:", font=("Helvetica", 16))
    date_label.pack(pady=5)
    cal = Calendar(expense_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    description_label = ctk.CTkLabel(expense_window, text="Description:", font=("Helvetica", 16))
    description_label.pack(pady=5)
    description_entry = ctk.CTkEntry(expense_window, width=300)
    description_entry.pack(pady=5)

    submit_button = ctk.CTkButton(expense_window, text="Add Expense", width=200, hover_color="green", command=lambda: submit_expense(amount_entry, category_entry, cal, description_entry, expense_window))
    submit_button.pack(pady=20)

def submit_expense(amount_entry, category_entry, cal, description_entry, window):
    date_selected = cal.get_date()
    add_expense(amount_entry.get(), category_entry.get(), date_selected, description_entry.get(), None)
    window.destroy()

# Function to view expenses in a table format
def open_view_expenses():
    expenses_window = ctk.CTkToplevel(app)
    expenses_window.title("View Expenses")
    expenses_window.geometry("600x400")

    tree = ttk.Treeview(expenses_window, columns=("ID", "Amount", "Category", "Date", "Description"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Date", text="Date")
    tree.heading("Description", text="Description")

    # Fetch expense data from the database
    expense_data = view_expenses()

    if expense_data is None:
        expense_data = []

    # Insert expense data into the table
    for expense in expense_data:
        tree.insert("", "end", values=expense)

    tree.pack(fill="both", expand=True)

# Function to handle adding income
def open_add_income():
    income_window = ctk.CTkToplevel(app)
    income_window.title("Add Income")
    income_window.geometry("400x500")

    amount_label = ctk.CTkLabel(income_window, text="Amount:", font=("Helvetica", 16))
    amount_label.pack(pady=5)
    amount_entry = ctk.CTkEntry(income_window, width=300)
    amount_entry.pack(pady=5)

    source_label = ctk.CTkLabel(income_window, text="Source:", font=("Helvetica", 16))
    source_label.pack(pady=5)
    source_entry = ctk.CTkEntry(income_window, width=300)
    source_entry.pack(pady=5)

    date_label = ctk.CTkLabel(income_window, text="Select Date:", font=("Helvetica", 16))
    date_label.pack(pady=5)
    cal = Calendar(income_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    description_label = ctk.CTkLabel(income_window, text="Description:", font=("Helvetica", 16))
    description_label.pack(pady=5)
    description_entry = ctk.CTkEntry(income_window, width=300)
    description_entry.pack(pady=5)

    submit_button = ctk.CTkButton(income_window, text="Add Income", width=200, hover_color="green", command=lambda: submit_income(amount_entry, source_entry, cal, description_entry, income_window))
    submit_button.pack(pady=20)

def submit_income(amount_entry, source_entry, cal, description_entry, window):
    date_selected = cal.get_date()
    add_income(amount_entry.get(), source_entry.get(), date_selected, description_entry.get())
    window.destroy()

# Function to view income in a table format
def open_view_income():
    income_window = ctk.CTkToplevel(app)
    income_window.title("View Income")
    income_window.geometry("600x400")

    tree = ttk.Treeview(income_window, columns=("ID", "Amount", "Source", "Date", "Description"), show='headings')
    tree.heading("ID", text="ID")
    tree.    heading("Amount", text="Amount")
    tree.heading("Source", text="Source")
    tree.heading("Date", text="Date")
    tree.heading("Description", text="Description")

    income_data = view_income()

    if income_data is None:
        income_data = []

    for income in income_data:
        tree.insert("", "end", values=income)

    tree.pack(fill="both", expand=True)

# Function to delete an expense
def open_delete_expense():
    delete_window = ctk.CTkToplevel(app)
    delete_window.title("Delete Expense")
    delete_window.geometry("600x400")

    tree = ttk.Treeview(delete_window, columns=("ID", "Amount", "Category", "Date", "Description"), show='headings', selectmode='extended')
    tree.heading("ID", text="ID")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Date", text="Date")
    tree.heading("Description", text="Description")

    expense_data = view_expenses()

    for expense in expense_data:
        tree.insert("", "end", values=expense)

    tree.pack(fill="both", expand=True)
    
    def delete_selected():
        selected_items = tree.selection()
        if selected_items:
            for item in selected_items:
                expense_id = tree.item(item, "values")[0]  # Get ID of selected expense
                delete_expense(int(expense_id))  # Delete expense from database
                tree.delete(item)  # Remove from treeview
            messagebox.showinfo("Success", "Selected expenses have been deleted.")
        else:
            messagebox.showwarning("Warning", "No expenses selected.")

    def delete_all():
        response = messagebox.askyesno("Confirmation", "Are you sure you want to delete all expenses?")
        if response:  # If the user confirms
            delete_all_expenses()  # Call the function to delete all expenses
            for item in tree.get_children():
                tree.delete(item)  # Clear the treeview
            messagebox.showinfo("Success", "All expenses have been deleted.")

    delete_button = ctk.CTkButton(delete_window, text="Delete Selected", width=200, hover_color="red", command=delete_selected)
    delete_button.pack(pady=10)

    delete_all_button = ctk.CTkButton(delete_window, text="Delete All Expenses", width=200, hover_color="red", command=delete_all)
    delete_all_button.pack(pady=10)

# Function to generate and display the interactive treemap chart
def view_expense_treemap():
    if not expense_data:
        messagebox.showinfo("No Data", "No expenses available to display.")
        return

    # Group expenses by category
    category_sums = defaultdict(float)
    subcategory_details = defaultdict(list)
    for expense in expense_data:
        category = expense[2]  # Main category
        amount = float(expense[1])
        description = expense[4]  # Subcategory (or description)
        category_sums[category] += amount
        subcategory_details[category].append((description, amount))

    labels = list(category_sums.keys())
    amounts = list(category_sums.values())

    # Create the treemap
    fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(sizes=amounts, label=labels, alpha=.8, ax=ax)
    ax.set_title("Expense Distribution by Category")
    plt.axis('off')

    def on_click(event):
        for i, rect in enumerate(ax.patches):
            if rect.contains(event)[0]:
                category = labels[i]
                result = analyze_category_spending(category, expense_data)
                add_chat_message(result, sender="Bot")
                
                # Now also list subcategories for the clicked category
                subcategory_result = list_subcategories(category, subcategory_details)
                add_chat_message(subcategory_result, sender="Bot")
                break

    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()

# Add Buttons
add_expense_button = ctk.CTkButton(app, text="Add Expense", width=250, hover_color="green", command=open_add_expense)
add_expense_button.pack(pady=15)

view_expense_button = ctk.CTkButton(app, text="View Expenses", width=250, hover_color="blue", command=open_view_expenses)
view_expense_button.pack(pady=15)

add_income_button = ctk.CTkButton(app, text="Add Income", width=250, hover_color="green", command=open_add_income)
add_income_button.pack(pady=15)

view_income_button = ctk.CTkButton(app, text="View Income", width=250, hover_color="blue", command=open_view_income)
view_income_button.pack(pady=15)

delete_expense_button = ctk.CTkButton(app, text="Delete Expense", width=250, hover_color="red", command=open_delete_expense)
delete_expense_button.pack(pady=15)

# Button to view treemap chart of expenses by category
view_treemap_button = ctk.CTkButton(app, text="View Expense Breakdown", width=250, hover_color="purple", command=view_expense_treemap)
view_treemap_button.pack(pady=15)

# Button to upload a file and process it
upload_file_button = ctk.CTkButton(app, text="Upload File", width=250, hover_color="orange", command=lambda: handle_chatbot_command("upload dataset"))
upload_file_button.pack(pady=15)

# Footer Label
footer_label = ctk.CTkLabel(app, text="Powered by Harsh, Aryan and Dheeraj", font=("Helvetica", 12))
footer_label.pack(pady=20)

# Start the application
app.mainloop()

