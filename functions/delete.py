import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "../commands.db")

def delete_database() -> None:
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    else:
        raise ValueError("No file found.")
