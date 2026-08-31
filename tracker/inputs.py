from datetime import datetime

from tracker.models import EXPENSE_CATEGORIES, INCOME_CATEGORIES, TYPES


def prompt_type() -> str:
    print("\nType:")
    for i, t in enumerate(TYPES, 1):
        print(f"  {i}. {t}")
    while True:
        choice = input("Select (1-2): ").strip()
        if choice in ("1", "2"):
            return TYPES[int(choice) - 1]
        print("  Invalid option. Try again.")


def prompt_amount() -> float:
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
    print("\nCategory:")
    for i, cat in enumerate(INCOME_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input(f"Select (1-{len(INCOME_CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(INCOME_CATEGORIES):
            return INCOME_CATEGORIES[int(choice) - 1]
        print("  Invalid option. Try again.")


def prompt_expense_category() -> str:
    print("\nCategory:")
    for i, cat in enumerate(EXPENSE_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input(f"Select (1-{len(EXPENSE_CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(EXPENSE_CATEGORIES):
            return EXPENSE_CATEGORIES[int(choice) - 1]
        print("  Invalid option. Try again.")


def prompt_note() -> str:
    note = input("\nNote (optional, press Enter to skip): ").strip()
    return note


def prompt_date() -> str:
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
    while True:
        year_inp = input("Type the Year :  ").strip()
        if year_inp.isdigit():
            year = int(year_inp)
            break
        print(f"{year_inp} is an Ivalid Year! || Please type a valid Year")
    return year


def prompt_day() -> int:
    while True:
        day_inp = input("Type the Day(1-31) :  ").strip()
        if day_inp.isdigit():
            day = int(day_inp)
            break
        print(f"{day_inp} is an Ivalid Day! || Please type a valid Day")
    return day


def prompt_month() -> int:
    while True:
        month_inp = input("Type the Month(1-12):  ").strip()
        if month_inp.isdigit() and 1 <= int(month_inp) <= 12:
            month = int(month_inp)
            break
        print("X Invalid Month. || Please select a number between 1 and 12!")
    return month
