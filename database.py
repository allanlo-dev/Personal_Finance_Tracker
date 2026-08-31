import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from tracker.models import Transaction

DB_NAME = Path(__file__).parent / "pct.db"


@contextmanager
def get_connection(db_path: str | Path = DB_NAME) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _row_to_transaction(row: sqlite3.Row) -> Transaction:
    return Transaction(
        id=row["id"],
        type=row["type"],
        amount=row["amount"],
        category=row["category"],
        note=row["note"],
        date=row["date"],
    )


def initialize_db() -> None:
    """Creates the transactions table if it doesn't exist."""
    with get_connection() as conn:
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


def add_transaction(transaction: Transaction) -> int:
    """Inserts a new transaction and returns its generated ID."""
    with get_connection() as conn:
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
        if new_id is None:
            raise ValueError("ID was not generated for the new transaction.")

    return new_id


def get_all_transactions() -> list[Transaction]:
    """Returns all transactions ordered by date descending."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, type, amount, category, note, date
            FROM transactions
            ORDER BY date DESC
        """)
        rows = cursor.fetchall()
    return [_row_to_transaction(row) for row in rows]


def get_transactions_of_last_30_days() -> list[Transaction]:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM transactions
        WHERE date BETWEEN date('now', '-30 days', 'localtime')
        AND date('now', 'localtime')
        ORDER BY date ASC;
        """)
        rows = cursor.fetchall()

    return [_row_to_transaction(row) for row in rows]


def get_transactions_by_category(category: str) -> list[Transaction]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM transactions
        WHERE category LIKE ?
        ORDER BY date ASC
        """
        cursor.execute(query, (category,))
        rows = cursor.fetchall()

    return [_row_to_transaction(row) for row in rows]


def get_transactions_by_type(t_type: str) -> list[Transaction]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM transactions
        WHERE type LIKE ?
        ORDER BY date ASC
        """
        cursor.execute(query, (t_type,))
        rows = cursor.fetchall()

    return [_row_to_transaction(row) for row in rows]


def get_transactions_by_date(search_date: str) -> list[Transaction]:

    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM transactions
        WHERE date LIKE ?
        ORDER BY date ASC;
        """
        cursor.execute(query, (search_date,))
        rows = cursor.fetchall()

    return [_row_to_transaction(row) for row in rows]
