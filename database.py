import random
import sqlite3
from calendar import monthrange
from datetime import date, datetime

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
    ORDER BY date ASC;
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


def seed_demo_transactions(
    start: date = date(2026, 1, 1),
    end: date | None = None,
    seed: int = 42,
) -> int:
    """Inserts demo transactions from `start` to `end` (default: today).

    Generates, per month:
      - Income  1200  Salary        on days 1 and 15
      - Expense  100  Internet-Data on day 3
      - Expense  500  Rent          on day 29 (clamped to the last day of the month)
      - Expense 50-200 Food         on 2 random days

    Dates outside the range are skipped. Returns the number of rows inserted.
    """
    if end is None:
        end = date.today()
    if start > end:
        raise ValueError("start must be on or before end")

    rng = random.Random(seed)  # same data on every run
    rows: list[Transaction] = []

    def add(
        day: int, t_type: str, amount: float, category: str, note: str, y: int, m: int
    ):
        day = min(day, monthrange(y, m)[1])  # e.g. 29 -> 28 in Feb 2026
        d = date(y, m, day)
        if start <= d <= end:
            rows.append(
                Transaction(
                    type=t_type,
                    amount=round(amount, 2),
                    category=category,
                    note=note,
                    date=d.isoformat(),
                )
            )

    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        add(1, "Income", 1200, "Salary", "Salary - first half", year, month)
        add(15, "Income", 1200, "Salary", "Salary - second half", year, month)
        add(3, "Expense", 100, "Internet-Data", "Monthly internet bill", year, month)
        add(29, "Expense", 500, "Rent", "Monthly rent", year, month)

        for day in sorted(rng.sample(range(2, monthrange(year, month)[1] + 1), 2)):
            add(day, "Expense", rng.uniform(50, 200), "Food", "Groceries", year, month)

        year, month = (year + 1, 1) if month == 12 else (year, month + 1)

    rows.sort(key=lambda t: t.date)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO transactions (type, amount, category, note, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        [(t.type, t.amount, t.category, t.note, t.date) for t in rows],
    )
    conn.commit()
    conn.close()
    return len(rows)
