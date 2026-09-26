import sqlite3
import random

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

    def seed_pets(self):
        """Inserts 100 random pets (Dogs and Cats) into the pets table if it's empty."""
        self.cursor.execute("SELECT COUNT(*) FROM pets")
        if self.cursor.fetchone()[0] > 0:
            print("Pets table already has data. Skipping seed script.")
            return

        dog_breeds = ['Aspin', 'Shih Tzu', 'Golden Retriever', 'German Shepherd', 'Poodle', 'Beagle']
        cat_breeds = ['Puspin', 'Persian', 'Siamese', 'Maine Coon', 'British Shorthair']
        
        dog_names = ['Bantay', 'Browny', 'Max', 'Charlie', 'Cooper', 'Buddy', 'Rocky', 'Thor', 'Lucky', 'Oscar']
        cat_names = ['Muning', 'Luna', 'Bella', 'Simba', 'Oliver', 'Milo', 'Tiger', 'Chloe', 'Lily', 'Shadow']

        pet_data = []
        for _ in range(100):
            species = random.choice(['Dog', 'Cat'])
            if species == 'Dog':
                name = random.choice(dog_names) + f"_{random.randint(1, 999)}"
                breed = random.choice(dog_breeds)
            else:
                name = random.choice(cat_names) + f"_{random.randint(1, 999)}"
                breed = random.choice(cat_breeds)
            
            age = random.randint(1, 15)
            status = 'Available'
            
            pet_data.append((name, species, breed, age, status))

        self.cursor.executemany("""
            INSERT INTO pets (name, species, breed, age, status)
            VALUES (?, ?, ?, ?, ?)
        """, pet_data)
        
        self.conn.commit()
        print("Successfully seeded 100 pets (Dogs and Cats) into the database!")

    def close(self):
        self.conn.close()