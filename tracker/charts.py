"""Matplotlib visualisations and the aggregation that feeds them.

The module is split in two halves:

* ``get_*_data`` functions reduce a list of transactions into plain
  ``{label: total}`` dictionaries. They are pure and do no drawing, which makes
  them straightforward to test on their own.
* ``generate_*`` functions take those dictionaries and render a figure. They
  block on :func:`matplotlib.pyplot.show` until the user closes the window, and
  release the figure afterwards.

A shared colour convention runs through both charts: teal (``#2DBDB1``) for
income and red (``#D23917``) for expenses.
"""

import matplotlib.pyplot as plt

from tracker.models import INCOME_CATEGORIES, TYPES, Transaction


def generate_chart(
    totals: dict[str, float], datetotals: dict[str, float], filter: str | None
) -> None:
    """Draw a two-panel figure for a single type or category.

    The left panel is a bar chart of totals; the right panel is a step plot of
    the amounts over time, annotated with each value. Both are tinted according
    to whether ``filter`` refers to income or to expenses.

    Args:
        totals: Mapping of type or category name to its summed amount, as
            returned by :func:`get_charts_data`.
        datetotals: Mapping of ISO date to the amount recorded on that date,
            also from :func:`get_charts_data`.
        filter: Label describing the current selection, used for the figure
            title and to pick the colour.

    Note:
        Blocks until the user closes the chart window.
    """
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
    """Draw a three-panel mosaic summarising a full set of transactions.

    The layout places the balance panel on the left, spanning the full height,
    with the income breakdown above the expense breakdown on the right.

    Args:
        totals: Income, expense and balance totals, as returned by
            :func:`get_mosaic_charts_data`.
        incometotals: Income totals per category.
        expensetotals: Expense totals per category.
        filter: Label describing the current selection, used as the figure
            title (for example ``"All Transactions"``).

    Note:
        Blocks until the user closes the chart window.
    """

    plt.style.use("ggplot")
    mosaic = """
    AB
    AC
    """
    colors = [
        "#2DBDB1" if t == "Income" else "#D23917" if t == "Expense" else "#1FC519"
        for t in totals
    ]

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
    """Aggregate transactions for :func:`generate_chart`.

    What the first dictionary groups by depends on ``filter``: when the user
    filtered by type the totals are grouped by type, otherwise they are grouped
    by category.

    Args:
        trans: Transactions to aggregate.
        filter: The active filter. If it is a member of
            :data:`~tracker.models.TYPES` the grouping is by type; any other
            value groups by category.

    Returns:
        A tuple of two mappings:

        * totals per type or per category, depending on ``filter``;
        * totals per ISO date.
    """
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
    """Aggregate transactions for :func:`generate_mosaic_chart`.

    Walks the list once, accumulating three views at the same time: the
    headline totals, the income breakdown and the expense breakdown. The
    running balance is added to the first mapping under the key ``"Balance"``,
    so it can be plotted alongside the income and expense bars.

    Args:
        trans: Transactions to aggregate.

    Returns:
        A tuple of three mappings:

        * totals per type, plus a ``"Balance"`` entry holding income minus
          expenses;
        * income totals per category;
        * expense totals per category.
    """
    transactions = trans

    totals: dict[str, float] = {}
    incometotals: dict[str, float] = {}
    expensetotals: dict[str, float] = {}
    balance: float = 0
    for t in transactions:
        cat: str = t.category
        typ: str = t.type
        totals[typ] = totals.get(typ, 0) + t.amount
        if t.type == "Income":
            incometotals[cat] = incometotals.get(cat, 0) + t.amount
            balance += t.amount
        else:
            expensetotals[cat] = expensetotals.get(cat, 0) + t.amount
            balance -= t.amount

    totals["Balance"] = balance
    return totals, incometotals, expensetotals


if __name__ == "__main__":
    pass
