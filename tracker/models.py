"""Core data structures and domain constants for the tracker.

This module defines the :class:`Transaction` dataclass, which is the single
record type used across the whole application, along with the closed
vocabularies for transaction types and categories. Every other module imports
its valid values from here, so adding a new category only requires editing
this file.
"""

from dataclasses import dataclass

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Rent",
    "Entertainment",
    "Internet-Data",
    "Others",
]
"""Valid categories for a transaction whose ``type`` is ``"Expense"``."""

INCOME_CATEGORIES = ["Salary", "Paycheck", "Others"]
"""Valid categories for a transaction whose ``type`` is ``"Income"``."""

TYPES = ["Income", "Expense"]
"""The two valid values for :attr:`Transaction.type`."""


@dataclass
class Transaction:
    """A single financial movement, either an income or an expense.

    This dataclass mirrors one row of the ``transactions`` table. Instances
    created in memory leave ``id`` as ``None``; the value is assigned by
    SQLite on insert and returned by
    :func:`database.add_transaction`.

    Attributes:
        type: Either ``"Income"`` or ``"Expense"``. See :data:`TYPES`.
        amount: Absolute value of the movement, always positive. The sign is
            derived from ``type`` at display time, never stored.
        category: A member of :data:`INCOME_CATEGORIES` or
            :data:`EXPENSE_CATEGORIES`, depending on ``type``.
        note: Free-text comment. May be an empty string or ``None``.
        date: Date of the movement as an ISO-8601 string (``YYYY-MM-DD``).
            Stored as text so that lexicographic ordering matches
            chronological ordering.
        id: Primary key assigned by the database, or ``None`` for a
            transaction that has not been persisted yet.
    """

    type: str  # 'Expense' or 'Income'
    amount: float
    category: str
    note: str | None
    date: str  # ISO format: YYYY-MM-DD
    id: int | None = None
