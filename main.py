from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_database():
    """
    Creates a SQLite database named 'books.db' with a table named 'books' if it does not already exist.
    
    The 'books' table has four columns: 'id', 'title', 'author', and 'pages_read', representing the book's unique identifier, title, author, and number of pages read, respectively.
    
    Parameters:
        None
    
    Returns:
        None
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, pages_read INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def book_list():
    """
    This function handles the root URL of the application, connecting to the SQLite database, 
    retrieving all books, and rendering the index.html template with the list of books.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    """
    Handles the HTTP POST request to add a new book to the database.
    
    Retrieves the title and author from the request form data, connects to the SQLite database,
    inserts the new book into the 'books' table, and commits the changes.
    
    Redirects the user to the book list page after a successful addition.
    
    Parameters:
        None (uses request.form data)
    
    Returns:
        A redirect response to the book list page
    """
    title = request.form['title']
    author = request.form['author']
    pages_read = request.form['pages_read']
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, pages_read) VALUES (?, ?, ?)', (title, author, pages_read))
    conn.commit()
    conn.close()
    return redirect(url_for('book_list'))

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    """
    Deletes a book from the database based on the provided book ID.

    Parameters:
        book_id (int): The ID of the book to be deleted.

    Returns:
        redirect: A redirect response to the book list page.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('book_list'))

@app.route('/done_today/<int:book_id>')
def done_today(book_id):
    """
    Updates the 'pages_read' field of a book in the database to 0 based on the provided book ID.

    Parameters:
        book_id (int): The ID of the book to be marked as done.

    Returns:
        redirect: A redirect response to the book list page.
    """
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('UPDATE books SET pages_read= 0 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('book_list'))

if __name__ == '__main__':
    create_database()
    app.run(debug=True)