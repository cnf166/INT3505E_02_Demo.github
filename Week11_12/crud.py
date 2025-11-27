from database import get_db

def get_books():
    db = get_db()
    cursor = db.execute("SELECT * FROM books ORDER BY id")
    return [dict(row) for row in cursor.fetchall()]

def get_book(book_id: int):
    db = get_db()
    cursor = db.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def create_book(book_data: dict):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (book_data["title"], book_data["author"], book_data.get("year"))
    )
    db.commit()
    book_data["id"] = cursor.lastrowid
    return book_data

def update_book(book_id: int, book_data: dict):
    db = get_db()
    db.execute(
        "UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",
        (book_data["title"], book_data["author"], book_data.get("year"), book_id)
    )
    db.commit()
    book_data["id"] = book_id
    return book_data

def delete_book(book_id: int):
    db = get_db()
    db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return True