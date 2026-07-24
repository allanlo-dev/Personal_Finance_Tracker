from database import initialize_db
from tracker.cli import run


if __name__ == "__main__":
    initialize_db()  # creates the DB and table if they don't exist
    run()
