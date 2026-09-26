from pet_system import PetSystem
from f import f

def main():
    app = PetSystem()
    comp = f()
    while True:
        print("\n=== Community Pet Adoption & Registry System ===")
        print("[1] Register Pet")
        print("[2] Search Pet")
        print("[3] Apply for Adoption")
        print("[4] Edit Pet Information")
        print("[5] Compatibility test")
        print("[0] Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            app.register_pet()
        elif choice == '2':
            app.search_pet()
        elif choice == '3':
            app.apply_adoption()
        elif choice == '4':
            app.edit_pet()
        elif choice == '5':
            comp.f()
        elif choice == '0':
            print("Exiting system. Goodbye!")
            app.db.close()
        else:
            print("Invalid choice! Please select between 1 and 4.")

if __name__ == "__main__":
    main()