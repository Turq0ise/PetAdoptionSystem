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
        keyword = input("Enter pet name, species, or breed to search (or press enter to display all): ").strip()
        query = f"%{keyword}%"
        
        self.db.cursor.execute(
            "SELECT pet_id, name, species, breed, age, status FROM pets WHERE name LIKE ? OR species LIKE ? OR breed LIKE ?",
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

        self.db.cursor.execute("SELECT status FROM pets WHERE pet_id = ?", (pet_id,))
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
        self.db.cursor.execute("UPDATE pets SET status = 'Adopted' WHERE pet_id = ?", (pet_id,))
        self.db.conn.commit()
        print(f"Success! Adoption application submitted for Pet ID {pet_id} by {adopter_name}.")

    def edit_pet(self):
        print("\n--- Use Case: Edit Pet Details ---")
        self.search_pet()
        
        try:
            pet_id = int(input("\nEnter the ID of the pet you want to edit: "))
        except ValueError:
            print("Invalid ID format.")
            return

        # Check if pet exists
        self.db.cursor.execute("SELECT pet_id, name, species, breed, age, status FROM pets WHERE pet_id = ?", (pet_id,))
        pet = self.db.cursor.fetchone()

        if not pet:
            print("Error: Pet ID not found.")
            return

        print(f"\nEditing Pet: [ID: {pet[0]}] Name: {pet[1]} | Species: {pet[2]} | Breed: {pet[3]} | Age: {pet[4]} | Status: {pet[5]}")
        print("Leave blank if you do not want to change a specific field.")

        # Get updated values
        new_name = input(f"Enter new name [{pet[1]}]: ").strip() or pet[1]
        new_species = input(f"Enter new species (Dog/Cat) [{pet[2]}]: ").strip() or pet[2]
        
        if new_species not in ['Dog', 'Cat']:
            print("Warning: Species is typically restricted to 'Dog' or 'Cat'. Keeping previous species or proceed carefully.")

        new_breed = input(f"Enter new breed [{pet[3]}]: ").strip() or pet[3]
        
        age_input = input(f"Enter new age [{pet[4]}]: ").strip()
        if age_input:
            try:
                new_age = int(age_input)
                if new_age < 0:
                    raise ValueError
            except ValueError:
                print("Invalid age entered. Keeping previous age.")
                new_age = pet[4]
        else:
            new_age = pet[4]

        new_status = input(f"Enter new status (Available/Adopted) [{pet[5]}]: ").strip() or pet[5]

        # Execute update in database
        self.db.cursor.execute("""
            UPDATE pets 
            SET name = ?, species = ?, breed = ?, age = ?, status = ?
            WHERE pet_id = ?
        """, (new_name, new_species, new_breed, new_age, new_status, pet_id))
        
        self.db.conn.commit()
        print(f"Success! Pet ID {pet_id} has been successfully updated.")