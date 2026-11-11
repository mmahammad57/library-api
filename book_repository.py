import db


def list_books(only_available):
    conn = db.connect()
    try:
        if only_available:
            return conn.execute("SELECT * FROM books WHERE available = 1").fetchall()
        return conn.execute("SELECT * FROM books").fetchall()
    finally:
        conn.close()


def get_book(book_id):
    conn = db.connect()
    try:
        return conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    finally:
        conn.close()


def create_book(title, author, isbn):
    conn = db.connect()
    try:
        cur = conn.execute(
            "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
            (title, author, isbn),
        )
        conn.commit()
        return conn.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone()
    finally:
        conn.close()


def delete_book(book_id):
    conn = db.connect()
    try:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
    finally:
        conn.close()


def count_books():
    conn = db.connect()
    try:
        return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    finally:
        conn.close()
