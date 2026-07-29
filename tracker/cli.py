import os
from datetime import datetime

from database import (
    add_transaction,
    get_all_transactions,
    get_transactions_by_month,
    get_transactions_of_last_30_days,
)
from tracker.models import EXPENSE_CATEGORIES, INCOME_CATEGORIES, TYPES, Transaction


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def display_header():
    print("\n" + "=" * 40)
    print("   Personal Finance Tracker (PCT)")
    print("=" * 40)


def display_menu():
    print("\nWhat do you want to do?")
    print("  1. Add transaction")
    print("  2. List all transactions")
    print("  3. List transactions of last 30 days")
    print("  4. List transactions by month")
    print("  0. Exit")


def display_balance(transactions):
    exp_transactions = 0
    inc_transactions = 0

    for t in transactions:
        if t.type == "Income":
            inc_transactions += t.amount

        else:
            exp_transactions += t.amount

    print("\n\n" + "=" * 40)
    print("             |BALANCE|")
    print("=" * 40 + "\n")

    print(f"The Total Income is: {inc_transactions}")
    print(f"The Total Expense is: {exp_transactions}")
    print(f"The Balance is: {inc_transactions - exp_transactions} \n")


def diplay_transactions(transactions):
    if not transactions:
        print("\n  No transactions found.")
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Type':<10} {'Amount':<10} {'Category':<18} Note")
    print("-" * 70)

    for t in transactions:
        sign = "+" if t.type == "Income" else "-"
        print(
            f"{t.id:<5} {t.date:<12} {t.type:<10} "
            f"{sign}${t.amount:<9.2f} {t.category:<18} {t.note or ''}"
        )


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
    note = input("Note (optional, press Enter to skip): ").strip()
    return note


def prompt_month() -> int:
    while True:
        month_inp = input("Select the Month(1-12):  ").strip()
        if month_inp.isdigit() and 1 <= int(month_inp) <= 12:
            month = int(month_inp)
            break
        print("X Invalid Month. || Please select a number between 1 and 12!")
    return month


def handle_add_transaction():
    print("\n--- New Transaction ---")
    t_type = prompt_type()
    amount = prompt_amount()
    if t_type == "Income":
        category = prompt_income_category()
    else:
        category = prompt_expense_category()

    note = prompt_note()
    today = datetime.now().astimezone().date().isoformat()

    transaction = Transaction(
        type=t_type,
        amount=amount,
        category=category,
        note=note,
        date=today,
    )

    new_id = add_transaction(transaction)
    print(f"\n  ✓ Transaction saved (ID: {new_id})")
    print(f"    {t_type.upper()} | ${amount:.2f} | {category} | {today}")


def handle_transactions_by_month():
    clear_terminal()
    month = prompt_month()
    transactions = get_transactions_by_month(month)

    diplay_transactions(transactions)
    display_balance(transactions)


def handle_list_transactions():
    clear_terminal()
    transactions = get_all_transactions()

    diplay_transactions(transactions)
    display_balance(transactions)


def list_transactions_of_last_30_days():
    clear_terminal()
    transactions = get_transactions_of_last_30_days()

    diplay_transactions(transactions)
    display_balance(transactions)


def run():
    display_header()
    while True:
        display_menu()
        choice = input("\nOption: ").strip()

        if choice == "1":
            handle_add_transaction()
        elif choice == "2":
            handle_list_transactions()
        elif choice == "3":
            list_transactions_of_last_30_days()
        elif choice == "4":
            handle_transactions_by_month()
        elif choice == "0":
            print("\nGoodbye!\n")
            break
        else:
            print("  Invalid option. Try again.")
