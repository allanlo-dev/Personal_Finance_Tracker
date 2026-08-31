import os

from database import (
    add_transaction,
    get_all_transactions,
    get_transactions_by_category,
    get_transactions_by_date,
    get_transactions_by_type,
    get_transactions_of_last_30_days,
)
from tracker.charts import (
    generate_chart,
    generate_mosaic_chart,
    get_charts_data,
    get_mosaic_charts_data,
)
from tracker.inputs import (
    prompt_amount,
    prompt_date,
    prompt_day,
    prompt_expense_category,
    prompt_income_category,
    prompt_month,
    prompt_note,
    prompt_type,
    prompt_year,
)
from tracker.models import TYPES, Transaction


def clear_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")  # noqa: S605  -No external input is used in a safe way


def display_header() -> None:
    print("\n" + "=" * 40)
    print("   Personal Finance Tracker (PCT)")
    print("=" * 40)


def display_menu() -> None:
    print("\n\nWhat do you want to do?")
    print("  1. Add transaction")
    print("  2. List all transactions")
    print("  3. List transactions of last 30 days")
    print("  4. List transactions by Date")
    print("  5. List transactions by Type/Category")
    print("  0. Exit")


def calculate_balance(transactions: list[Transaction]) -> tuple[float, float, float]:
    income = sum(t.amount for t in transactions if t.type == "Income")
    expense = sum(t.amount for t in transactions if t.type == "Expense")
    balance = income - expense
    return income, expense, balance


def display_chart() -> bool:
    while True:
        print("\nDo you want to display this data in a chart?")
        print("1. Yes")
        print("2. No")
        choice = input("=> ").strip()
        if choice.isdigit() and choice == "1":
            return True

        elif choice.isdigit() and choice == "2":
            return False
        else:
            print("Invalid option. Please select 1 or 2.")


def display_balance(transactions: list[Transaction]) -> None:
    income, expense, balance = calculate_balance(transactions)
    print("\n\n" + "=" * 40)
    print("             |BALANCE|")
    print("=" * 40 + "\n")

    print(f"The Total Income is: {income}")
    print(f"The Total Expense is: {expense}")
    print(f"The Balance is: {balance} \n")


def display_transactions(transactions: list[Transaction]) -> None:
    if not transactions:
        print("\n  No transactions found.")
        return

    print("\n" + "=" * 70)
    print("                     ||TRANSACTIONS||")
    print("=" * 70 + "\n")
    print(f"\n{'ID':<5} {'Date':<12} {'Type':<10} {'Amount':<10} {'Category':<18} Note")
    print("-" * 70)

    for t in transactions:
        sign = "+" if t.type == "Income" else "-"
        print(
            f"{t.id:<5} {t.date:<12} {t.type:<10} "
            f"{sign}${t.amount:<9.2f} {t.category:<18} {t.note or ''}"
        )


def search_by_date_menu() -> str:
    print("\nSearch Transactions by:")
    while True:
        print("1. a Specific Date")
        print("2. a Specific Month")
        print("3. a Specific Year")

        date_choice = input("\nChoose a date filter: ").strip()

        if date_choice.isdigit() and date_choice == "1":
            year = prompt_year()
            month = prompt_month()
            day = prompt_day()
            search_date = f"{year}-{month:02d}-{day:02d}"
            break
        elif date_choice.isdigit() and date_choice == "2":
            year = prompt_year()
            month = prompt_month()
            search_date = f"{year}-{month:02d}-%"
            break
        elif date_choice.isdigit() and date_choice == "3":
            year = prompt_year()
            search_date = f"{year}-%-%"
            break
        else:
            print("  Invalid option. Try again.")

    return search_date


def search_by_type_category_menu() -> str:
    print("\nSearch Transactions by:")
    type = prompt_type()
    while True:
        print("\n\nDo you want to filter by a specific category?")
        print("1. Yes")
        print(f"2. No. List all transaction by: {type}")
        type_choice = input("\nChoose an option: ").strip()
        if type_choice.isdigit() and type_choice == "1":
            category = (
                prompt_income_category()
                if type == "Income"
                else prompt_expense_category()
            )
            return category
        elif type_choice.isdigit() and type_choice == "2":
            return type
        else:
            print("  Invalid option. Try again.")


def handle_add_transaction() -> None:
    print("\n--- New Transaction ---")
    t_type = prompt_type()
    amount = prompt_amount()
    if t_type == "Income":
        category = prompt_income_category()
    else:
        category = prompt_expense_category()

    note = prompt_note()

    date = prompt_date()
    transaction = Transaction(
        type=t_type,
        amount=amount,
        category=category,
        note=note,
        date=date,
    )

    new_id = add_transaction(transaction)
    print(f"\n  ✓ Transaction saved (ID: {new_id})")
    print(f"    {t_type.upper()} | ${amount:.2f} | {category} | {date}")


def handle_all_transactions() -> None:
    clear_terminal()
    transactions = get_all_transactions()

    display_transactions(transactions)
    if transactions:
        display_balance(transactions)
        if display_chart():
            totals, incometotals, expensetotals = get_mosaic_charts_data(transactions)
            generate_mosaic_chart(
                totals, incometotals, expensetotals, filter="All Transactions"
            )


def handle_transactions_by_date() -> None:
    clear_terminal()
    search_date = search_by_date_menu()
    transactions = get_transactions_by_date(search_date)
    display_transactions(transactions)
    if transactions:
        display_balance(transactions)
        if display_chart():
            totals, incometotals, expensetotals = get_mosaic_charts_data(transactions)
            generate_mosaic_chart(
                totals,
                incometotals,
                expensetotals,
                filter=f"Transactions of {search_date}",
            )


def handle_transactions_of_last_30_days() -> None:
    clear_terminal()
    transactions = get_transactions_of_last_30_days()

    display_transactions(transactions)
    if transactions:
        display_balance(transactions)
        if display_chart():
            totals, incometotals, expensetotals = get_mosaic_charts_data(transactions)
            generate_mosaic_chart(
                totals,
                incometotals,
                expensetotals,
                filter="Transactions of Last 30 Days",
            )


def handle_transactions_by_type_category() -> None:
    clear_terminal()
    search_type_category = search_by_type_category_menu()
    if search_type_category in TYPES:
        type = search_type_category
        transactions = get_transactions_by_type(type)
    else:
        category = search_type_category
        transactions = get_transactions_by_category(category)

    display_transactions(transactions)
    total: float = 0
    for t in transactions:
        total += t.amount
    if transactions:
        print("\n" + "=" * 40)
        print("               |TOTAL|")
        print("=" * 40 + "\n")
        print(f"The Total is: {total}\n")
        if display_chart():
            totals, datetotals = get_charts_data(
                transactions, filter=search_type_category
            )
            generate_chart(totals, datetotals, filter=search_type_category)


def run() -> None:
    display_header()
    while True:
        display_menu()
        choice = input("\nOption: ").strip()

        if choice == "1":
            handle_add_transaction()
        elif choice == "2":
            handle_all_transactions()
        elif choice == "3":
            handle_transactions_of_last_30_days()
        elif choice == "4":
            handle_transactions_by_date()
        elif choice == "5":
            handle_transactions_by_type_category()
        elif choice == "0":
            print("\nGoodbye!\n")
            break
        else:
            print("  Invalid option. Try again.")
