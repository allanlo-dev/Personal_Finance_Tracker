"""Persistence layer: SQLite connection handling and transaction queries.

This module is the only place in the application that talks to SQLite. It
exposes a small, typed API that returns :class:`~tracker.models.Transaction`
objects, so the rest of the codebase never handles raw rows or SQL.

All queries use parameter substitution (``?`` placeholders) rather than string
interpolation, which keeps the application safe from SQL injection.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from tracker.models import Transaction

DB_NAME = Path(__file__).parent / "pct.db"
"""Absolute path to the SQLite file, anchored to this module's directory.

Resolving the path from ``__file__`` rather than the current working directory
means the application always opens the same database, no matter where it is
launched from.
"""


@contextmanager
def get_connection(db_path: str | Path = DB_NAME) -> Iterator[sqlite3.Connection]:
    """Yield a SQLite connection, committing on success and always closing.

    The connection is configured with :class:`sqlite3.Row` as its row factory,
    so query results can be accessed by column name. On leaving the ``with``
    block without an exception the transaction is committed; the connection is
    closed in either case, including when the body raises.

    Args:
        db_path: Database file to open. Defaults to :data:`DB_NAME`. Pass
            ``":memory:"`` to run against a throwaway in-memory database,
            which is useful in tests.

    Yields:
        An open connection to ``db_path``.

    Example:
        >>> with get_connection() as conn:
        ...     rows = conn.cursor().execute("SELECT 1").fetchall()
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _row_to_transaction(row: sqlite3.Row) -> Transaction:
    """Convert a database row into a :class:`~tracker.models.Transaction`.

    Private helper shared by every query function, so the column-to-field
    mapping is defined in exactly one place.

    Args:
        row: A row from the ``transactions`` table.

    Returns:
        The equivalent ``Transaction`` instance.
    """
    return Transaction(
        id=row["id"],
        type=row["type"],
        amount=row["amount"],
        category=row["category"],
        note=row["note"],
        date=row["date"],
    )


def initialize_db() -> None:
    """Create the ``transactions`` table if it does not already exist.

    Safe to call on every start-up: the statement is a no-op when the table is
    present, so it never destroys existing data.
    """
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
    """Insert a transaction and return the ID assigned by the database.

    The ``id`` field of ``transaction`` is ignored; SQLite generates the
    primary key.

    Args:
        transaction: The transaction to persist. Its ``id`` may be ``None``.

    Returns:
        The auto-generated primary key of the new row.

    Raises:
        ValueError: If SQLite does not report a generated row ID, which would
            mean the insert did not take effect.
    """
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
    """Return every stored transaction, newest first.

    Returns:
        All transactions ordered by date descending. Empty if the table has no
        rows.
    """
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
    """Return the transactions dated within the last 30 days.

    The window is computed by SQLite itself using the machine's local time, so
    the boundaries follow the user's timezone rather than UTC. Both ends of the
    range are inclusive.

    Returns:
        Matching transactions ordered by date ascending.
    """
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
    """Return the transactions belonging to a given category.

    Args:
        category: Category to match, normally a member of
            :data:`~tracker.models.INCOME_CATEGORIES` or
            :data:`~tracker.models.EXPENSE_CATEGORIES`. SQL wildcards (``%``
            and ``_``) are honoured because the comparison uses ``LIKE``.

    Returns:
        Matching transactions ordered by date ascending.
    """
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
    """Return every transaction of a given type.

    Args:
        t_type: Either ``"Income"`` or ``"Expense"``. See
            :data:`~tracker.models.TYPES`.

    Returns:
        Matching transactions ordered by date ascending.
    """
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
    """Return the transactions matching a date pattern.

    Because dates are stored as ``YYYY-MM-DD`` text, a trailing ``%`` wildcard
    turns an exact-date lookup into a month or year lookup.

    Args:
        search_date: A ``LIKE`` pattern over the stored date. For example
            ``"2026-03-15"`` for a single day, ``"2026-03-%"`` for a whole
            month, or ``"2026-%"`` for a whole year.

    Returns:
        Matching transactions ordered by date ascending.
    """

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
