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

    ax.set_title("Income and Expenses", fontweight="bold", fontsize=16)
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()
    plt.close(fig)


def generate_mosaic_chart(
    totals: dict[str, float],
    incometotals: dict[str, float],
    expensetotals: dict[str, float],
) -> None:

    plt.style.use("ggplot")
    mosaic = """
    AB
    AC
    """
    colors = ["#2DBDB1" if t == "Income" else "#D23917" for t in totals]

    fig, axd = plt.subplot_mosaic(mosaic, figsize=(10, 5), layout="constrained")

    totalsbar = axd["A"].bar(
        list(totals.keys()),
        list(totals.values()),
        color=colors,
        edgecolor="black",
        width=0.6,
    )
    axd["A"].bar_label(totalsbar, fmt="${:,.0f}", padding=3)
    axd["A"].set_title("BALANCE", fontweight="bold", fontsize=16)

    incomesbar = axd["B"].bar(
        list(incometotals.keys()),
        list(incometotals.values()),
        color="#2DBDB1",
        edgecolor="black",
        width=0.6,
    )
    axd["B"].bar_label(incomesbar, fmt="${:,.0f}", padding=3)
    axd["B"].set_title("INCOMES", fontweight="bold", fontsize=16)

    expensesbar = axd["C"].bar(
        list(expensetotals.keys()),
        list(expensetotals.values()),
        color="#D23917",
        edgecolor="black",
        width=0.6,
    )
    axd["C"].bar_label(expensesbar, fmt="${:,.0f}", padding=3)
    axd["C"].set_title("EXPENSES", fontweight="bold", fontsize=16)

    for ax in axd.values():
        ax.set_ylabel("Monto ($)")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(True)
        ax.set_axisbelow(True)

    plt.show()
    plt.close(fig)


def get_charts_data(
    trans: list[Transaction],
) -> tuple[dict[str, float], dict[str, float], dict[str, float]]:
    transactions = trans

    totals: dict[str, float] = {}
    incometotals: dict[str, float] = {}
    expensetotals: dict[str, float] = {}
    for t in transactions:
        cat: str = t.category
        typ: str = t.type
        totals[typ] = totals.get(typ, 0) + t.amount
        if t.type == "Income":
            incometotals[cat] = incometotals.get(cat, 0) + t.amount

        else:
            expensetotals[cat] = expensetotals.get(cat, 0) + t.amount

    return totals, incometotals, expensetotals


if __name__ == "__main__":
    pass
