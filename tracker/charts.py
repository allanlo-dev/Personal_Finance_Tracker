import matplotlib.pyplot as plt

from tracker.models import Transaction


def generate_chart(amounts: dict[str, float]) -> None:
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    barras = ax.bar(
        list(amounts.keys()),
        list(amounts.values()),
        color="#2DBDB1",
        edgecolor="black",
        width=0.6,
    )
    ax.bar_label(barras, fmt="${:,.0f}", padding=3)

    ax.set_title("Expenses by Category", fontweight="bold", fontsize=16)
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()
    plt.close(fig)


def generate_chart_by_month(trans: list[Transaction]) -> None:
    transactions = trans

    icnometotals: dict[str, float] = {}
    expensetotals: dict[str, float] = {}
    for t in transactions:
        cat: str = t.category
        if t.type == "Income":
            icnometotals[cat] = icnometotals.get(cat, 0) + t.amount
            
        else:
            expensetotals[cat] = expensetotals.get(cat, 0) + t.amount

    generate_chart(expensetotals)
    generate_chart(icnometotals)


if __name__ == "__main__":
    pass
