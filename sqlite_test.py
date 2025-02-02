import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Run a query
cursor.execute('SELECT * FROM Employees')

# Fetch and print all rows
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
