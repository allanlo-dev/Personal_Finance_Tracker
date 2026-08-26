import matplotlib.pyplot as plt

from tracker.models import INCOME_CATEGORIES, TYPES, Transaction


def generate_chart(
    totals: dict[str, float], datetotals: dict[str, float], filter: str | None
) -> None:
    plt.style.use("ggplot")
    colors = [
        "#2DBDB1" if filter in INCOME_CATEGORIES or filter == TYPES[0] else "#D23917"
    ]
    fig, axs = plt.subplots(1, 2, figsize=(11, 5), layout="constrained")
    fig.suptitle(f"{filter} Transactions", fontweight="bold", fontsize=18)

    totalbar = axs[0].bar(
        list(totals.keys()),
        list(totals.values()),
        color=colors,
        edgecolor="black",
        width=0.3,
    )
    axs[0].bar_label(totalbar, fmt="${:,.0f}", padding=4)
    axs[0].set_title("Total", fontweight="bold", fontsize=16)

    axs[1].plot(
        list(datetotals.keys()),
        list(datetotals.values()),
        marker="o",
        drawstyle="steps-post",
        color="#2DBDB1"
        if filter in INCOME_CATEGORIES or filter == TYPES[0]
        else "#D23917",
    )
    for date, amount in datetotals.items():
        axs[1].annotate(
            f"${amount:,.0f}",
            xy=(date, amount),
            xytext=(-13, 3),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )
    axs[1].set_title("Date of Transactions", fontweight="bold", fontsize=16)
    axs[1].set_xlabel("(YY-MM-DD)")
    fig.autofmt_xdate()

    for ax in axs:
        ax.set_ylabel("Monto ($)")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(True)
        ax.set_axisbelow(True)

    plt.show()
    plt.close(fig)


def generate_mosaic_chart(
    totals: dict[str, float],
    incometotals: dict[str, float],
    expensetotals: dict[str, float],
    filter: str | None,
) -> None:

    plt.style.use("ggplot")
    mosaic = """
    AB
    AC
    """
    colors = ["#2DBDB1" if t == "Income" else "#D23917" for t in totals]

    fig, axd = plt.subplot_mosaic(mosaic, figsize=(10, 5), layout="constrained")
    fig.suptitle(f"{filter}", fontweight="bold", fontsize=18)
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
    filter: str,
) -> tuple[dict[str, float], dict[str, float]]:
    transactions = trans
    typetotals: dict[str, float] = {}
    categorytotals: dict[str, float] = {}
    datetotals: dict[str, float] = {}

    if filter in TYPES:
        for t in transactions:
            typ: str = t.type
            typetotals[typ] = typetotals.get(typ, 0) + t.amount

            date = t.date
            datetotals[date] = datetotals.get(date, 0) + t.amount
        return typetotals, datetotals

    else:
        for t in transactions:
            cat: str = t.category
            categorytotals[cat] = categorytotals.get(cat, 0) + t.amount

            date = t.date
            datetotals[date] = datetotals.get(date, 0) + t.amount
        return categorytotals, datetotals


def get_mosaic_charts_data(
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
