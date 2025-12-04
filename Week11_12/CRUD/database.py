import sqlite3
import os

DATABASE_PATH = "books.db"

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE_PATH):
        conn = get_db()
        conn.execute("""
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            )
        """)
        # Sample data
        conn.executemany(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            [
                ("The Hobbit", "J.R.R. Tolkien", 1937),
                ("1984", "George Orwell", 1949),
                ("Clean Code", "Robert C. Martin", 2008),
            ]
        )
        conn.commit()
        conn.close()