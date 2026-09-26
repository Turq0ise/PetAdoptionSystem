import sqlite3
<<<<<<< HEAD
import random
=======
from pathlib import Path
from datetime import date
>>>>>>> 7a9942429f48c5927e95d80a58d0e4ccdd06b7eb

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "pet_adoption.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            breed TEXT NOT NULL,
            age REAL NOT NULL CHECK (age >= 0),
            sex TEXT NOT NULL CHECK (sex IN ('Male', 'Female')),
            description TEXT,
            photo TEXT,
            status TEXT NOT NULL DEFAULT 'Available'
                CHECK (status IN ('Available', 'Pending', 'Adopted')),
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            contact TEXT NOT NULL,
            address TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS adoption_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL,
            pet_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            application_date TEXT NOT NULL,
            decision_date TEXT,
            adoption_date TEXT,
            status TEXT NOT NULL DEFAULT 'Pending'
                CHECK (status IN ('Pending', 'Approved', 'Rejected')),
            FOREIGN KEY (applicant_id) REFERENCES applicants(id),
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        );
        """
    )

    count = conn.execute("SELECT COUNT(*) AS c FROM pets").fetchone()["c"]
    if count == 0:
        conn.executemany(
            """
            INSERT INTO pets
            (name, species, breed, age, sex, description, photo, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Mochi", "Dog", "Shih Tzu", 2, "Female",
                    "Sweet, cuddly, and loves being around people.",
                    None, "Available", date.today().isoformat()
                ),
                (
                    "Simba", "Cat", "Domestic Shorthair", 1.5, "Male",
                    "Quiet, curious, and happiest in a cozy indoor home.",
                    None, "Available", date.today().isoformat()
                ),
                (
                    "Brownie", "Dog", "Aspin", 3, "Male",
                    "Playful, loyal, and always ready for a walk.",
                    None, "Available", date.today().isoformat()
                ),
            ],
        )

    conn.commit()
    conn.close()


def dashboard_stats():
    conn = get_db()
    data = {
        "total": conn.execute("SELECT COUNT(*) AS c FROM pets").fetchone()["c"],
        "available": conn.execute(
            "SELECT COUNT(*) AS c FROM pets WHERE status='Available'"
        ).fetchone()["c"],
        "pending": conn.execute(
            "SELECT COUNT(*) AS c FROM adoption_applications WHERE status='Pending'"
        ).fetchone()["c"],
        "adopted": conn.execute(
            "SELECT COUNT(*) AS c FROM pets WHERE status='Adopted'"
        ).fetchone()["c"],
    }
    conn.close()
    return data


def recent_applications(limit=5):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT aa.id, aa.application_date, aa.status,
               a.full_name, p.name AS pet_name
        FROM adoption_applications aa
        JOIN applicants a ON a.id = aa.applicant_id
        JOIN pets p ON p.id = aa.pet_id
        ORDER BY aa.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return rows


def list_pets(search="", status="All"):
    conn = get_db()
    sql = "SELECT * FROM pets WHERE 1=1"
    params = []

    if search.strip():
        sql += " AND (name LIKE ? OR breed LIKE ? OR species LIKE ?)"
        term = f"%{search.strip()}%"
        params.extend([term, term, term])

    if status != "All":
        sql += " AND status = ?"
        params.append(status)

    sql += " ORDER BY id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def get_pet(pet_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM pets WHERE id=?", (pet_id,)).fetchone()
    conn.close()
    return row


def add_pet(name, species, breed, age, sex, description, photo=None):
    conn = get_db()
    conn.execute(
        """
        INSERT INTO pets
        (name, species, breed, age, sex, description, photo, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Available', ?)
        """,
        (
            name, species, breed, age, sex, description, photo,
            date.today().isoformat()
        ),
    )
    conn.commit()
    conn.close()


def update_pet(pet_id, name, species, breed, age, sex, description, status, photo):
    conn = get_db()
    conn.execute(
        """
        UPDATE pets
        SET name=?, species=?, breed=?, age=?, sex=?,
            description=?, status=?, photo=?
        WHERE id=?
        """,
        (
            name, species, breed, age, sex,
            description, status, photo, pet_id
        ),
    )
    conn.commit()
    conn.close()


def create_application(pet_id, full_name, email, contact, address, reason):
    conn = get_db()

    pet = conn.execute("SELECT status FROM pets WHERE id=?", (pet_id,)).fetchone()
    if not pet or pet["status"] == "Adopted":
        conn.close()
        raise ValueError("This pet is no longer available for adoption.")

    existing = conn.execute(
        """
        SELECT aa.id
        FROM adoption_applications aa
        JOIN applicants a ON a.id = aa.applicant_id
        WHERE aa.pet_id=?
          AND LOWER(a.email)=LOWER(?)
          AND aa.status='Pending'
        """,
        (pet_id, email),
    ).fetchone()

    if existing:
        conn.close()
        raise ValueError("This applicant already has a pending request for this pet.")

    cursor = conn.execute(
        """
        INSERT INTO applicants (full_name, email, contact, address)
        VALUES (?, ?, ?, ?)
        """,
        (full_name, email, contact, address),
    )
    applicant_id = cursor.lastrowid

    conn.execute(
        """
        INSERT INTO adoption_applications
        (applicant_id, pet_id, reason, application_date, status)
        VALUES (?, ?, ?, ?, 'Pending')
        """,
        (applicant_id, pet_id, reason, date.today().isoformat()),
    )

    conn.execute(
        "UPDATE pets SET status='Pending' WHERE id=? AND status='Available'",
        (pet_id,),
    )

    conn.commit()
    conn.close()


def list_applications(search="", status="All"):
    conn = get_db()
    sql = """
        SELECT aa.*, a.full_name, a.email, a.contact, a.address,
               p.name AS pet_name, p.species, p.breed
        FROM adoption_applications aa
        JOIN applicants a ON a.id = aa.applicant_id
        JOIN pets p ON p.id = aa.pet_id
        WHERE 1=1
    """
    params = []

    if search.strip():
        term = f"%{search.strip()}%"
        sql += " AND (a.full_name LIKE ? OR a.email LIKE ? OR p.name LIKE ?)"
        params.extend([term, term, term])

    if status != "All":
        sql += " AND aa.status=?"
        params.append(status)

    sql += " ORDER BY aa.id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def get_application(application_id):
    conn = get_db()
    row = conn.execute(
        """
        SELECT aa.*, a.full_name, a.email, a.contact, a.address,
               p.name AS pet_name, p.species, p.breed, p.age, p.sex,
               p.status AS pet_status
        FROM adoption_applications aa
        JOIN applicants a ON a.id=aa.applicant_id
        JOIN pets p ON p.id=aa.pet_id
        WHERE aa.id=?
        """,
        (application_id,),
    ).fetchone()
    conn.close()
    return row


def approve_application(application_id):
    conn = get_db()
    application = conn.execute(
        "SELECT * FROM adoption_applications WHERE id=?",
        (application_id,),
    ).fetchone()

    if not application or application["status"] != "Pending":
        conn.close()
        raise ValueError("Only pending applications can be approved.")

    conn.execute(
        """
        UPDATE adoption_applications
        SET status='Approved', decision_date=?, adoption_date=?
        WHERE id=?
        """,
        (date.today().isoformat(), date.today().isoformat(), application_id),
    )

    conn.execute(
        """
        UPDATE adoption_applications
        SET status='Rejected', decision_date=?
        WHERE pet_id=? AND id<>? AND status='Pending'
        """,
        (date.today().isoformat(), application["pet_id"], application_id),
    )

    conn.execute(
        "UPDATE pets SET status='Adopted' WHERE id=?",
        (application["pet_id"],),
    )

    conn.commit()
    conn.close()


def reject_application(application_id):
    conn = get_db()
    application = conn.execute(
        "SELECT * FROM adoption_applications WHERE id=?",
        (application_id,),
    ).fetchone()

    if not application or application["status"] != "Pending":
        conn.close()
        raise ValueError("Only pending applications can be rejected.")

    conn.execute(
        """
        UPDATE adoption_applications
        SET status='Rejected', decision_date=?
        WHERE id=?
        """,
        (date.today().isoformat(), application_id),
    )

    remaining = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM adoption_applications
        WHERE pet_id=? AND status='Pending'
        """,
        (application["pet_id"],),
    ).fetchone()["c"]

    if remaining == 0:
        pet = conn.execute(
            "SELECT status FROM pets WHERE id=?",
            (application["pet_id"],),
        ).fetchone()
        if pet and pet["status"] != "Adopted":
            conn.execute(
                "UPDATE pets SET status='Available' WHERE id=?",
                (application["pet_id"],),
            )

<<<<<<< HEAD
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
=======
    conn.commit()
    conn.close()


def adoption_history():
    conn = get_db()
    rows = conn.execute(
        """
        SELECT aa.id, aa.adoption_date,
               a.full_name, a.email,
               p.name AS pet_name, p.species, p.breed
        FROM adoption_applications aa
        JOIN applicants a ON a.id=aa.applicant_id
        JOIN pets p ON p.id=aa.pet_id
        WHERE aa.status='Approved'
        ORDER BY aa.adoption_date DESC, aa.id DESC
        """
    ).fetchall()
    conn.close()
    return rows
>>>>>>> 7a9942429f48c5927e95d80a58d0e4ccdd06b7eb
