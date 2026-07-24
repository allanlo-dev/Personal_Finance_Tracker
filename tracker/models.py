from dataclasses import dataclass

CATEGORIES = [
    "Comida",
    "Transporte",
    "Renta",
    "Entretenimiento",
    "Internet-Data",
    "Otros",
]

TYPES = ["gasto", "ingreso"]


@dataclass
class Transaction:
    """Represents a single financial transaction."""

    type: str  # 'gasto' or 'ingreso'
    amount: float
    category: str
    note: str
    date: str  # ISO format: YYYY-MM-DD
    id: int = None
