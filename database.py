import sqlite3
from datetime import datetime

from tracker.models import Transaction

DB_NAME = "pct.db"


def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # allows accessing columns by name
    return conn


def initialize_db():
    """Creates the transactions table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            type     TEXT    NOT NULL,
            amount   REAL    NOT NULL,
            category TEXT    NOT NULL,
            note     TEXT,
            date     TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_transaction(transaction: Transaction) -> int:
    """Inserts a new transaction and returns its generated ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (type, amount, category, note, date)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            transaction.type,
            transaction.amount,
            transaction.category,
            transaction.note,
            transaction.date,
        ),
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_all_transactions() -> list[Transaction]:
    """Returns all transactions ordered by date descending."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, type, amount, category, note, date
        FROM transactions
        ORDER BY date DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        Transaction(
            id=row["id"],
            type=row["type"],
            amount=row["amount"],
            category=row["category"],
            note=row["note"],
            date=row["date"],
        )
        for row in rows
    ]


def get_transactions_of_last_30_days():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM transactions 
    WHERE date BETWEEN date('now', '-30 days', 'localtime') AND date('now', 'localtime')
    ORDER BY date ASC;
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        Transaction(
            id=row["id"],
            type=row["type"],
            amount=row["amount"],
            category=row["category"],
            note=row["note"],
            date=row["date"],
        )
        for row in rows
    ]


def get_transactions_by_month(month: int):
    year = datetime.now().year
    search_date = f"{year}-{month:02d}-%"
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT * FROM transactions
    WHERE date LIKE ?
    ORDER BY date ASC
    """
    cursor.execute(query, (search_date,))
    rows = cursor.fetchall()

    return [
        Transaction(
            id=row["id"],
            type=row["type"],
            amount=row["amount"],
            category=row["category"],
            note=row["note"],
            date=row["date"],
        )
        for row in rows
    ]
