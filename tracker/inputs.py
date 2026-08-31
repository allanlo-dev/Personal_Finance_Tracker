"""Interactive prompts that read and validate user input from the terminal.

Every function here follows the same contract: it loops until the user supplies
an acceptable value, printing an explanatory message on each failed attempt,
and only then returns. None of them ever raise on bad input, so callers can
treat the returned value as already validated.

Keeping the prompts in their own module lets :mod:`tracker.cli` deal purely
with flow and presentation.
"""

from datetime import datetime

from tracker.models import EXPENSE_CATEGORIES, INCOME_CATEGORIES, TYPES


def prompt_type() -> str:
    """Ask the user to choose a transaction type.

    Returns:
        The selected member of :data:`~tracker.models.TYPES`, either
        ``"Income"`` or ``"Expense"``.
    """
    print("\nType:")
    for i, t in enumerate(TYPES, 1):
        print(f"  {i}. {t}")
    while True:
        choice = input("Select (1-2): ").strip()
        if choice in ("1", "2"):
            return TYPES[int(choice) - 1]
        print("  Invalid option. Try again.")


def prompt_amount() -> float:
    """Ask the user for a monetary amount.

    Rejects anything that is not a number as well as zero and negative values,
    since the sign of a movement is carried by its type, not its amount.

    Returns:
        A strictly positive amount.
    """
    while True:
        raw = input("Amount ($): ").strip()
        try:
            value = float(raw)
            if value <= 0:
                print("  Amount must be greater than 0.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid number.")


def prompt_income_category() -> str:
    """Ask the user to choose a category for an income.

    Returns:
        The selected member of :data:`~tracker.models.INCOME_CATEGORIES`.
    """
    print("\nCategory:")
    for i, cat in enumerate(INCOME_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input(f"Select (1-{len(INCOME_CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(INCOME_CATEGORIES):
            return INCOME_CATEGORIES[int(choice) - 1]
        print("  Invalid option. Try again.")


def prompt_expense_category() -> str:
    """Ask the user to choose a category for an expense.

    Returns:
        The selected member of :data:`~tracker.models.EXPENSE_CATEGORIES`.
    """
    print("\nCategory:")
    for i, cat in enumerate(EXPENSE_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input(f"Select (1-{len(EXPENSE_CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(EXPENSE_CATEGORIES):
            return EXPENSE_CATEGORIES[int(choice) - 1]
        print("  Invalid option. Try again.")


def prompt_note() -> str:
    """Ask the user for an optional free-text note.

    Returns:
        The note with surrounding whitespace stripped, or an empty string if
        the user pressed Enter without typing anything.
    """
    note = input("\nNote (optional, press Enter to skip): ").strip()
    return note


def prompt_date() -> str:
    """Ask the user for a full date, one component at a time.

    Collects year, month and day separately and then validates the combination
    with :meth:`datetime.datetime.strptime`, which rejects impossible dates
    such as February 30th. On rejection the whole sequence starts over.

    Returns:
        The confirmed date as an ISO-8601 string (``YYYY-MM-DD``), ready to be
        stored in :attr:`~tracker.models.Transaction.date`.
    """
    while True:
        print("\n\n")
        year = prompt_year()
        month = prompt_month()
        day = prompt_day()
        date = f"{year}-{month:02d}-{day:02d}"
        try:
            checked_date = datetime.strptime(date, "%Y-%m-%d")
            print(f"    ✓ Date Saved {date}")
            return checked_date.strftime("%Y-%m-%d")
        except ValueError:
            print("X Error: Type a valid date or use the correct format (YYYY-MM-DD)\n")


def prompt_year() -> int:
    """Ask the user for a year.

    Only checks that the input is numeric; whether the resulting date exists is
    decided by :func:`prompt_date`.

    Returns:
        The year as an integer.
    """
    while True:
        year_inp = input("Type the Year :  ").strip()
        if year_inp.isdigit():
            year = int(year_inp)
            break
        print(f"{year_inp} is an Ivalid Year! || Please type a valid Year")
    return year


def prompt_day() -> int:
    """Ask the user for a day of the month.

    Only checks that the input is numeric; whether the day is valid for the
    chosen month is decided by :func:`prompt_date`.

    Returns:
        The day as an integer.
    """
    while True:
        day_inp = input("Type the Day(1-31) :  ").strip()
        if day_inp.isdigit():
            day = int(day_inp)
            break
        print(f"{day_inp} is an Ivalid Day! || Please type a valid Day")
    return day


def prompt_month() -> int:
    """Ask the user for a month number.

    Returns:
        The month as an integer between 1 and 12 inclusive.
    """
    while True:
        month_inp = input("Type the Month(1-12):  ").strip()
        if month_inp.isdigit() and 1 <= int(month_inp) <= 12:
            month = int(month_inp)
            break
        print("X Invalid Month. || Please select a number between 1 and 12!")
    return month
