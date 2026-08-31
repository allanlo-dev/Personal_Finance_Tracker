"""Application entry point.

Prepares the database and hands control to the interactive menu. Run it with::

    python main.py
"""

from database import initialize_db
from tracker.cli import run

if __name__ == "__main__":
    initialize_db()  # creates the DB and table if they don't exist
    run()
