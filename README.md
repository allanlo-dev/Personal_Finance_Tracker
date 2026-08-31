# Personal Finance Tracker (PFT)

A command-line application to track personal expenses and income, built with
Python, SQLite and matplotlib.

## Features (v1)

- Add income and expenses with type, amount, category, note and date
- List all transactions in an aligned table view
- Filter by date: a specific day, a whole month, or a whole year
- Filter by type (Income / Expense) and optionally by a single category
- List the transactions of the last 30 days
- Balance summary (income vs. expenses) for any set of results
- Optional charts for every listing, rendered with matplotlib

## Planned Features

- Export to CSV
- REST API with FastAPI (v2)

## Tech Stack

- Python 3.13+
- SQLite3 (built-in)
- matplotlib — charts
- [uv](https://docs.astral.sh/uv/) — dependency and environment management
- ruff, mypy and pre-commit — linting, formatting and type checking

## Setup

The project is managed with **uv**, which creates the virtual environment and
installs the locked dependencies in one step:

```bash
# Clone the repo
git clone git@github.com:allanlo-dev/Personal_Finance_Tracker.git
cd personal-finance-tracker

# Create the environment and install dependencies from uv.lock
uv sync

# Run the app
uv run python main.py
```

<details>
<summary>Alternative: plain venv + pip</summary>

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

</details>

### Development

Install the dev tools and enable the git hooks:

```bash
uv sync --group dev
uv run pre-commit install
```

Run the checks manually at any time:

```bash
uv run ruff check .     # lint
uv run ruff format .    # format
uv run mypy .           # type check (strict settings in pyproject.toml)
```

## Usage

Running `main.py` creates `pct.db` next to the script if it does not exist,
then opens the main menu:

| Option | Action                                                                   |
|--------|--------------------------------------------------------------------------|
| 1      | Add a transaction — prompts for type, amount, category, note and date     |
| 2      | List all transactions, with balance and an optional chart                |
| 3      | List the transactions of the last 30 days                                |
| 4      | List transactions by date — a specific day, month or year                |
| 5      | List transactions by type, optionally narrowed to one category           |
| 0      | Exit                                                                     |

After any listing the app offers to draw a chart of the results. Options 2–4
produce a three-panel mosaic (balance, income by category, expenses by
category); option 5 produces a two-panel figure with the total and its evolution
over time.

### Categories

Categories are fixed lists defined in `tracker/models.py`:

- **Income** — Salary, Paycheck, Others
- **Expense** — Food, Transport, Rent, Entertainment, Internet-Data, Others

## Data Model

Every record is a `Transaction` (`tracker/models.py`), stored in a single
`transactions` table:

| Column     | Type    | Notes                                                  |
|------------|---------|--------------------------------------------------------|
| `id`       | INTEGER | Primary key, assigned automatically                    |
| `type`     | TEXT    | `Income` or `Expense`                                  |
| `amount`   | REAL    | Always positive; the sign is derived from `type`       |
| `category` | TEXT    | Must belong to the list matching `type`                |
| `note`     | TEXT    | Optional free text                                     |
| `date`     | TEXT    | ISO-8601 (`YYYY-MM-DD`), so text ordering = date order |

The database file is `pct.db`, resolved relative to `database.py` so the app
always opens the same file regardless of the working directory. It is excluded
from version control by `.gitignore`.

## Project Structure

```
personal-finance-tracker/
├── main.py                  # Entry point: initializes the DB and starts the menu
├── database.py              # SQLite connection handling and all queries
├── pyproject.toml           # Project metadata, dependencies, ruff and mypy config
├── uv.lock                  # Locked dependency versions
├── .pre-commit-config.yaml  # ruff + mypy git hooks
├── tracker/
│   ├── __init__.py
│   ├── models.py            # Transaction dataclass and domain constants
│   ├── inputs.py            # Validated terminal prompts
│   ├── cli.py               # Menus, formatting and the main loop
│   └── charts.py            # Aggregation and matplotlib figures
```

### Architecture

The layers only depend downwards, which keeps each one testable on its own:

```
main.py  →  tracker/cli.py  →  tracker/inputs.py   (user input)
                            →  tracker/charts.py   (visualisation)
                            →  database.py         (persistence)
                                      ↓
                            tracker/models.py      (shared data types)
```

`database.py` is the only module that executes SQL, and every query uses
parameter substitution rather than string interpolation.

## Author

Allan Isaac Lopez Serrano
