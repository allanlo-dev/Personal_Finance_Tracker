import matplotlib.pyplot as plt

from tracker.models import Transaction


def generate_chart_by_month(trans: list[Transaction]) -> None:
    transactions = trans

    icnometotals :dict[str,float] = {}
    expensetotals :dict[str,float] = {}
    for t in transactions:
        cat :str= t.category
        if t.type == "Income":
            icnometotals[cat] = icnometotals.get(cat, 0) +t.amount
        else:
            expensetotals[cat] = expensetotals.get(cat, 0) +t.amount

    fig, ax = plt.subplots(figsize=(10, 5), layout ="constrained")
    plt.style.use("ggplot")
    ax.bar(list(icnometotals.keys()), list(icnometotals.values()))

    ax.set_title("Incomes")
    ax.grid(True)
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    pass