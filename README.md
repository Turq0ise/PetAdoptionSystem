# PawMatch — Pet Adoption Management System

A cute desktop Pet Adoption Management System built with **Python + CustomTkinter + SQLite**.

## Features

- Cute pastel CustomTkinter interface
- Dashboard with pet/adoption statistics
- Add and edit pets
- Upload pet photos
- Search pets
- Filter by adoption status
- Submit adoption applications
- Email/contact validation
- Prevent duplicate pending applications
- Review applications
- Approve or reject applications
- Automatically mark approved pets as Adopted
- Automatically reject other pending applications for the same pet
- Adoption history
- SQLite database

## Run the Program

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
python app.py
```

## Project Structure

```text
pet_adoption_customtkinter/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── documentation.md
├── .gitignore
├── assets/
│   └── uploads/
│       └── .gitkeep
└── ui/
    ├── __init__.py
    ├── theme.py
    ├── components.py
    ├── dashboard.py
    ├── pets.py
    ├── applications.py
    └── history.py
```

## Practical Exam Requirements Covered

- Real-world problem: manual pet adoption records
- System proposal
- Functional and non-functional requirements
- Search function
- Data validation
- User-friendly interface
- Database
- Source code
- Minimum 3 use cases
- Challenges and limitations
