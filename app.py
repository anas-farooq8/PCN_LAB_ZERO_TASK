from flask import Flask, request, render_template
import sqlite3
import pandas as pd

# Create a Flask app
app = Flask(__name__)

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('books_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the data with optional search by title or rating
# Need both GET and POST methods to display the data and search
@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all the books
    query = 'SELECT * FROM books'
    search_title = request.form.get('title')
    search_rating = request.form.get('rating')

    # If search by title or rating, add WHERE clause to the query
    if search_title:
        query += f" WHERE Title LIKE '%{search_title}%'"
    elif search_rating:
        query += f" WHERE Star_Rating = {float(search_rating)}"

    # Execute the query
    cursor.execute(query)
    books = cursor.fetchall()
    conn.close()

    return render_template('index.html', books=books)

# Route to add a new book
if __name__ == '__main__':
    app.run(debug=True)
