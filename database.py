import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "equipment.db"
SCHEMA = BASE_DIR / "schema.sql"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    with open(SCHEMA, "r", encoding="utf-8") as file:
        connection.executescript(file.read())

    # Add simple starter data only when the equipment table is empty.
    count = connection.execute(
        "SELECT COUNT(*) AS count FROM equipment"
    ).fetchone()["count"]

    if count == 0:
        connection.executemany(
            """
            INSERT INTO equipment
            (name, category, total_quantity, available_quantity)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Laptop", "Electronics", 5, 5),
                ("Projector", "Electronics", 3, 3),
                ("Extension Cord", "Accessories", 8, 8),
            ],
        )

    connection.commit()
    connection.close()
