# Personal Finance Tracker (PCT)

A command-line application to track personal expenses and income, built with Python and SQLite.

## Features (v1)
- Add expenses and income with category and note
- Automatically records the date of each transaction
- List all transactions in a clean table view
- Filter transactions by month
- Filter transactions of the last 30 days
- Monthly balance summary (income vs expenses)
- Demo data seeder to populate the database for testing

## Planned Features
- Filter transactions by date range
- Summary breakdown by category
- Show balance in charts
- REST API with FastAPI (v2)

## Tech Stack
- Python 3.11+
- SQLite3 (built-in)

## Setup

```bash
# Clone the repo
git clone git@github.com:allanlo-dev/Personal_Finance_Tracker.git
cd personal-finance-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py

#(OPTIONAL)Choice the number 5 to Add Demo Data in the database to Test
```

## Demo Data

To try the app with a database that already has history, use  |5. Add Demo Transactions to Test|  in the menu. It fills the range `2026-01-01` through today with:

| Type    | Amount  | Category      | When                                   |
|---------|---------|---------------|----------------------------------------|
| Income  | 1200    | Salary        | 1st and 15th of each month             |
| Expense | 100     | Internet-Data | 3rd of each month                      |
| Expense | 500     | Rent          | 29th of each month                     |
| Expense | 50–200  | Food          | 2 random days per month                |



Notes:
- Amounts and the random Food dates are seeded from a fixed value, so repeated
  runs produce identical data.
- The rent day is clamped to the last day of short months (e.g. Feb 28 in 2026).
- Dates after the end of the range are skipped.
- Running it more than once will insert duplicates — reset `pct.db` first.

## Project Structure

```
personal-finance-tracker/
├── main.py          # Entry point
├── database.py      # SQLite connection and queries
├── requirements.txt
├── tracker/
│   ├── models.py    # Transaction dataclass and constants
│   └── cli.py       # Interactive menu and user input
```
