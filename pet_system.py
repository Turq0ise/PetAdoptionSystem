import re
from database import DatabaseManager

class PetSystem:
    def __init__(self):
        self.db = DatabaseManager()

    def validate_phone(self, phone):
        # Validates a standard 11-digit mobile number format (e.g., 09123456789)
        return bool(re.match(r"^09\d{9}$", phone))

    def register_pet(self):
        print("\n--- Use Case 1: Register a New Pet ---")
        name = input("Enter Pet Name: ").strip()
        species = input("Enter Species (Dog/Cat/etc.): ").strip()
        breed = input("Enter Breed: ").strip()
        
        while True:
            try:
                age = int(input("Enter Age (years): "))
                if age < 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please enter a valid positive integer for age.")

        if not name or not species or not breed:
            print("Error: Fields cannot be empty! Data validation failed.")
            return

        self.db.cursor.execute(
            "INSERT INTO pets (name, species, breed, age) VALUES (?, ?, ?, ?)",
            (name, species, breed, age)
        )
        self.db.conn.commit()
        print(f"Success! Pet '{name}' has been successfully registered.")

    def search_pet(self):
        print("\n--- Use Case 2: Search Function ---")
        keyword = input("Enter pet name, species, or breed to search: ").strip()
        query = f"%{keyword}%"
        
        self.db.cursor.execute(
            "SELECT id, name, species, breed, age, status FROM pets WHERE name LIKE ? OR species LIKE ? OR breed LIKE ?",
            (query, query, query)
        )
        results = self.db.cursor.fetchall()

        if not results:
            print("No matching pets found.")
        else:
            print("\n{:<5} {:<15} {:<12} {:<15} {:<5} {:<10}".format("ID", "Name", "Species", "Breed", "Age", "Status"))
            print("-" * 65)
            for row in results:
                print("{:<5} {:<15} {:<12} {:<15} {:<5} {:<10}".format(row[0], row[1], row[2], row[3], row[4], row[5]))

    def apply_adoption(self):
        print("\n--- Use Case 3: Submit Adoption Application ---")
        self.search_pet()
        
        try:
            pet_id = int(input("\nEnter the ID of the pet you want to adopt: "))
        except ValueError:
            print("Invalid ID format.")
            return

        self.db.cursor.execute("SELECT status FROM pets WHERE id = ?", (pet_id,))
        pet = self.db.cursor.fetchone()

        if not pet:
            print("Error: Pet ID not found.")
            return
        if pet[0] != 'Available':
            print("Error: Selected pet is no longer available for adoption.")
            return

        adopter_name = input("Enter Adopter's Full Name: ").strip()
        contact_number = input("Enter Contact Number (e.g., 09123456789): ").strip()

        if not self.validate_phone(contact_number):
            print("Error: Invalid contact number format. Must be 11 digits starting with 09. Data validation failed.")
            return

        self.db.cursor.execute(
            "INSERT INTO adoptions (pet_id, adopter_name, contact_number) VALUES (?, ?, ?)",
            (pet_id, adopter_name, contact_number)
        )
        self.db.cursor.execute("UPDATE pets SET status = 'Adopted' WHERE id = ?", (pet_id,))
        self.db.conn.commit()
        print(f"Success! Adoption application submitted for Pet ID {pet_id} by {adopter_name}.")