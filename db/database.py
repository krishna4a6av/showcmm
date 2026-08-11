import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "../commands.db")

def is_initialized() -> bool:
    if not os.path.exists(DB_FILE):
        return False

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='commands'"
        )
        table_exists = cursor.fetchone()
        conn.close()
        return bool(table_exists)
    except sqlite3.Error:
        return False

def initialize() -> None:
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT UNIQUE,
                count INTEGER DEFAULT 1
            )
        """)

def insert_commands_bulk(commands: list[str]) -> None:
    initialize()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.executemany("""
            INSERT INTO commands(command,count)
            VALUES(?,1)
            ON CONFLICT(command)
            DO UPDATE SET count=count+1
            """, [(cmd,) for cmd in commands])


def get_all_commands() -> list[tuple[str, int]]:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT command, count FROM commands ORDER BY count DESC")
            rows = cursor.fetchall()
        return rows
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return []

def get_filter_commands(query: str) -> list[tuple[str, int]] :
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT command, count
                FROM commands
                WHERE command LIKE ?
                ORDER BY count DESC""",(f"%{query}%",),)
            rows = cursor.fetchall()
        return rows
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return []

def delete_database() -> bool:
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        return True
    else:
        return False
