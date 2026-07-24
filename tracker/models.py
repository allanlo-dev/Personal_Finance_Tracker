from dataclasses import dataclass

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Rent",
    "Entertainment",
    "Internet-Data",
    "Others",
]

INCOME_CATEGORIES = ["Salary", "Paycheck", "Others"]

TYPES = ["Income", "Expense"]


@dataclass
class Transaction:
    """Represents a single financial transaction."""

    type: str  # 'Expense' or 'Income'
    amount: float
    category: str
    note: str
    date: str  # ISO format: YYYY-MM-DD
    id: int = None
