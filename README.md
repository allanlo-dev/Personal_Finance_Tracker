# Personal Finance Tracker (PCT)

A command-line application to track personal expenses and income, built with Python and SQLite.

## Features (v1)
- Add expenses and income with category and note
- Automatically records the date of each transaction
- List all transactions in a clean table view
- Filter transactions by month
- Filter transactions of the last 30 days

## Planned Features
- Filter transactions by date range or month
- Monthly balance summary (income vs expenses)
- Summary breakdown by category
- Show balance in charts
- REST API with FastAPI (v2)

## Tech Stack
- Python 3.11+
- SQLite3 (built-in)

## Setup

```bash
# Clone the repo
git clone https://github.com/your-username/personal-finance-tracker.git
cd personal-finance-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

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
