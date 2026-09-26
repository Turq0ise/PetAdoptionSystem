# PawMatch — Pet Adoption Management System
## Practical Exam Documentation

## 1. System Proposal

### Problem
Small shelters and animal welfare groups may record adoptable pets and applicants manually through paper forms, spreadsheets, or social media messages. This can lead to missing information, duplicate requests, and confusion about whether a pet is still available.

### Proposed Solution
PawMatch is a desktop Pet Adoption Management System that stores pet and adoption records in one SQLite database. It helps staff add pets, search records, review applicants, and track completed adoptions.

## 2. Functional Requirements

- Add a pet.
- Edit pet details.
- Upload a pet photo.
- Search pets by name, breed, or species.
- Filter pets by adoption status.
- Submit an adoption application.
- Validate applicant information.
- Review all applications.
- Approve or reject applications.
- Automatically change pet status after approval.
- View adoption history.

## 3. Non-Functional Requirements

- User-friendly and visually clear interface.
- Fast enough for a small organization.
- Simple local database.
- Organized source code for maintenance.
- Parameterized database queries and validated inputs.

## 4. Main Use Cases

### Use Case 1 — Add Pet
Staff enters pet information and optionally selects a photo. The system validates the information and saves it.

### Use Case 2 — Search Pet
Staff searches by pet name, species, or breed and can filter by status.

### Use Case 3 — Process Adoption
An application is submitted. Staff reviews it and approves or rejects it. On approval, the pet automatically becomes Adopted.

## 5. Testing

### Test 1
Add a pet with complete valid information.

**Expected:** The pet appears on the Pets page.

### Test 2
Submit an application using an invalid email address.

**Expected:** The system displays an error and does not save the application.

### Test 3
Approve a pending application.

**Expected:** Application becomes Approved, pet becomes Adopted, and other pending requests for that pet become Rejected.

## 6. Challenges and Limitations

### Challenges
- Keeping application and pet statuses synchronized.
- Validating applicant input.
- Handling pet photo files.
- Designing a clear desktop interface.

### Limitations
- No staff login yet.
- No email or SMS notifications.
- No online payments.
- No cloud synchronization.
- Intended for a small local shelter or school project.

## 7. Future Features

- Staff login and roles
- Vaccination/medical record checklist
- Meet-and-greet appointment scheduling
- Printable adoption certificate
- Reports and charts
- Email notifications
