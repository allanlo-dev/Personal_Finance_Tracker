import matplotlib.pyplot as plt

from tracker.models import Transaction


def generate_chart_by_month(trans: list[Transaction]) -> None:
    transactions = trans

    exp_transactions: float = 0
    inc_transactions: float = 0
    income = []
    expense = []

    for t in transactions:
        if t.type == "Income":
            inc_transactions += t.amount
        else:
            exp_transactions += t.amount

    income.append(inc_transactions)
    expense.append(exp_transactions)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(6, income, label="Incomes")
    ax.bar(6, expense, label="Expenses")

    ax.set_title("Monthly Balance")
    ax.legend()
    ax.grid(True)
    plt.show()
