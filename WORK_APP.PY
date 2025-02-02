from flask import Flask, render_template, request, jsonify
import sqlite3
import re
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('company.db')

# Function to execute SQL queries
def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Function to process user query and generate SQL
def process_query(user_query):
    user_query = user_query.lower()

    if "show me all employees in the" in user_query:
        department = re.search(r"show me all employees in the (.+?) department", user_query)
        if department:
            department_name = department.group(1).strip()
            return f"SELECT * FROM Employees WHERE LOWER(Department) = LOWER(?);", (department_name,)
        else:
            return "Sorry, I couldn't understand the department name. Please try again."

    elif "who is the manager of the" in user_query:
        department = re.search(r"who is the manager of the (.+?) department", user_query)
        if department:
            department_name = department.group(1).strip()
            return f"SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER(?);", (department_name,)
        else:
            return "Sorry, I couldn't understand the department name. Please try again."

    elif "list all employees hired after" in user_query:
        date = re.search(r"list all employees hired after (\d{4}-\d{2}-\d{2})", user_query)
        if date:
            hire_date = date.group(1).strip()
            try:
                datetime.strptime(hire_date, '%Y-%m-%d')
                return f"SELECT * FROM Employees WHERE Hire_Date > ?;", (hire_date,)
            except ValueError:
                return "Oops! It looks like the date format is incorrect.  Please use YYYY-MM-DD "
        else:
            return "Sorry, I couldn't understand the date. Please try again."

    elif "what is the total salary expense for the" in user_query:
        department = re.search(r"what is the total salary expense for the (.+?) department", user_query)
        if department:
            department_name = department.group(1).strip()
            return f"SELECT SUM(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?);", (department_name,)
        else:
            return "Sorry, I couldn't understand the department name. Please try again."

    else:
        return "Sorry, I couldn't understand your query. Can you rephrase?"


# Home route to render the chat UI
@app.route('/')
def home():
    return render_template('index.html')

# Route to process the chat query
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('user_query')
    result = process_query(user_query)

    if isinstance(result, tuple):  # If the result is a tuple (sql, params)
        sql, params = result
        if sql.startswith("SELECT"):
            query_result = execute_query(sql, params)
            if isinstance(query_result, str):  # If there’s an error message (not a list of results)
                return jsonify({'response': query_result})
            if query_result:
                return jsonify({'response': query_result})
            else:
                return jsonify({'response': 'No results found. Please take a moment to review the spelling and try again.'})
    else:
        return jsonify({'response': result})  # Return the error message directly


if __name__ == '__main__':
    app.run(debug=True)
