import sqlite3

class DatabaseManager:
    def __init__(self, db_name="pet_adoption.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT DEFAULT 'Mixed Breed',
                age INTEGER NOT NULL,
                status TEXT DEFAULT 'Available'
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS adoptions (
                adoption_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER,
                adopter_name TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                FOREIGN KEY(pet_id) REFERENCES pets(pet_id)
            )
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()