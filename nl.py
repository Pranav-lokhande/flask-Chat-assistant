import sqlite3
import nltk
import re
from datetime import datetime

# Initialize NLTK (you can use more advanced NLP libraries like spaCy later)
nltk.download('punkt')

# Connect to SQLite database
def connect_db():
    return sqlite3.connect('company.db')

# Function to execute queries and fetch results
def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Process the query and generate SQL
def process_query(user_query):
    # Normalize the query to lower case for easier processing
    user_query = user_query.lower()

    if "show me all employees in the" in user_query:
        department = re.search(r"show me all employees in the (.+?) department", user_query)
        if department:
            department_name = department.group(1).strip()
            return f"SELECT * FROM Employees WHERE Department = ?;", (department_name,)
        else:
            return "Sorry, I couldn't understand the department name. Please try again."

    elif "who is the manager of the" in user_query:
        department = re.search(r"who is the manager of the (.+?) department", user_query)
        if department:
            department_name = department.group(1).strip()
            return f"SELECT Manager FROM Departments WHERE Name = ?;", (department_name,)
        else:
            return "Sorry, I couldn't understand the department name. Please try again."

    elif "list all employees hired after" in user_query:
        date = re.search(r"list all employees hired after (\d{4}-\d{2}-\d{2})", user_query)
        if date:
            hire_date = date.group(1).strip()
            try:
                # Validate the date format
                datetime.strptime(hire_date, '%Y-%m-%d')
                return f"SELECT * FROM Employees WHERE Hire_Date > ?;", (hire_date,)
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD format."
        else:
            return "Sorry, I couldn't understand the date. Please try again."

    elif "what is the total salary expense for the" in user_query:
        department = re.search(r"what is the total salary expense for the (.+?) department", user_query)
        if department:
            department_name = department.group(1).strip()
            return f"SELECT SUM(Salary) FROM Employees WHERE Department = ?;", (department_name,)
        else:
            return "Sorry, I couldn't understand the department name. Please try again."

    else:
        return "Sorry, I couldn't understand your query. Can you rephrase?"

# Main function to interact with the user
def chat_assistant():
    print("Hello! I'm your chat assistant. How can I help you?")

    while True:
        user_input = input("You: ")
        print(f"You typed: {user_input}")  # Debugging line to check input
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        sql, params = process_query(user_input)
        print(f"SQL Query: {sql}")  # Debugging line to check generated SQL
        
        if sql.startswith("SELECT"):
            result = execute_query(sql, params)
            
            if result:
                print("Assistant: Here are the results:")
                for row in result:
                    print(row)
            else:
                print("Assistant: No results found.")
        else:
            print(f"Assistant: {sql}")


# Run the as
