import pandas as pd
from tkinter import filedialog, messagebox

# Function to clean the data
def clean_expense_data():
    file_path = r'C:\Users\LENOVO\OneDrive\Desktop\Expense_Tracker\Dataset\expense_data_updated.xlsx'  # Path to dataset file
    df = pd.read_excel(file_path)

    # Reorganize and rename the columns as required
    columns_to_extract = {
        'Amount': 'Amount',
        'Category': 'Category',
        'Date': 'Date',
        'Note': 'Description'  
    }

    # Extract and reorder the columns
    df_cleaned = df[list(columns_to_extract.keys())]
    df_cleaned = df_cleaned.rename(columns=columns_to_extract)

    # Save the cleaned and reordered data to a new Excel file
    output_file_path = r'C:\Users\LENOVO\OneDrive\Desktop\Expense_Tracker\Dataset\Cleaned_Data_ET_1.xlsx'
    df_cleaned.to_excel(output_file_path, index=False)

    return f"Cleaned data saved to {output_file_path}"

# Function to clear the chat screen
def clear_screen(chat_display):
    chat_display.configure(state="normal")
    chat_display.delete(1.0, "end")
    chat_display.configure(state="disabled")

# Function to analyze spending in a specific category
def analyze_category_spending(category, expense_data):
    category_total = sum(float(expense[1]) for expense in expense_data if expense[2].lower() == category.lower())
    return f"Total spending in {category}: {category_total}"

# Function to find the category with the highest spending
def get_highest_spending_category(expense_data):
    category_sums = {}
    for expense in expense_data:
        category = expense[2]
        amount = float(expense[1])
        if category in category_sums:
            category_sums[category] += amount
        else:
            category_sums[category] = amount

    highest_category = max(category_sums, key=category_sums.get)
    return f"Highest spending is in {highest_category}: {category_sums[highest_category]}"

def list_subcategories(category, subcategory_details):
    if category not in subcategory_details:
        return f"No subcategories found under {category}."
    
    subcategories = [f"{desc} ({amt})" for desc, amt in subcategory_details[category]]
    subcategory_list = "\n".join(subcategories)
    return f"Subcategories under {category}:\n{subcategory_list}"

# Function to handle file upload via chatbot
def upload_dataset_via_chatbot():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                return "Unsupported file format."

            # Process and return the data
            return data
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return "No file selected."

# Function to list available commands
def list_commands():
    commands = [
        "clean data - Clean and reorganize the dataset.",
        "clear screen - Clear the chatbot display.",
        "analyze <category> - Analyze spending in a specific category.",
        "highest spending - Find out which category has the highest spending.",
        "upload dataset - Upload a new dataset for analysis.",
        "generate chart - Generate a treemap chart of expenses.",
        "help - Show this list of available commands.",
        "how to do that? - To export dataset."
    ]
    return "Available commands:\n" + "\n".join(commands)

# Updated process_command function to handle listing subcategories and file uploads
def process_command(command, expense_data=None, chat_display=None, subcategory_details=None):
    command = command.strip().lower()

    if command == "upload dataset":
        data = upload_dataset_via_chatbot()
        if isinstance(data, pd.DataFrame):
            # If data was successfully loaded, you might want to process and update expense_data
            expense_data.clear()
            subcategory_details.clear()
            for index, row in data.iterrows():
                expense_data.append((None, row['Amount'], row['Category'], row['Date'], row['Description']))
                subcategory_details[row['Category']].append((row['Description'], row['Amount']))
            return "Dataset uploaded and processed successfully."
        else:
            return data

    elif command == "generate chart":
        if expense_data:
            return "Generating the treemap chart..."
        else:
            return "No data available. Please upload a dataset first."

    elif command == "clean data":
        return clean_expense_data()

    elif command == "clear screen" and chat_display:
        clear_screen(chat_display)
        return "Screen cleared."

    elif command.startswith("analyze "):
        category = command.split("analyze ", 1)[1]
        return analyze_category_spending(category, expense_data)

    elif command == "highest spending":
        return get_highest_spending_category(expense_data)

    elif command == "help":
        return list_commands()
    
    elif command == "how to upload dataset?" or command == "how to do that?" or command == "how to get the dataset?":
        return ("Use this link to get your transaction file from Google Pay - https://support.google.com/googlepay/answer/9015738?hl=en")

    else:
        return "Sorry, I don't understand that command. Try 'help' to get a list of commands."
