from pathlib import Path
import re
import shutil
import uuid

import customtkinter as ctk
from tkinter import filedialog, messagebox

from database import (
    list_pets,
    add_pet,
    update_pet,
    get_pet,
    create_application,
)
from ui.theme import COLORS
from ui.components import (
    page_title,
    make_card,
    status_pill,
    clear_children,
    cute_button,
    load_pet_image,
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "assets" / "uploads"


def validate_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


def validate_contact(contact):
    cleaned = re.sub(r"[\s()+-]", "", contact)
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def copy_photo(source):
    if not source:
        return None

    src = Path(source)
    if src.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Please choose a PNG, JPG, JPEG, or WEBP photo.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    target = UPLOAD_DIR / f"{uuid.uuid4().hex}{src.suffix.lower()}"
    shutil.copy2(src, target)
    return str(target)


class PetsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew")
        top.grid_columnconfigure(0, weight=1)

        title = page_title(
            top,
            "Pet management",
            "Meet the cuties 🐾",
            "Search pets, add new profiles, and manage adoption status.",
        )
        title.grid(row=0, column=0, sticky="w")

        cute_button(
            top,
            "＋ Add Pet",
            command=self.open_add_pet,
            width=120,
        ).grid(row=0, column=1, sticky="e")

        filters = make_card(self)
        filters.grid(row=1, column=0, sticky="ew", pady=(18, 14))
        filters.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Search name, breed, or species...",
            height=40,
            corner_radius=13,
            border_color=COLORS["line"],
        )
        self.search_entry.grid(
            row=0, column=0, padx=(16, 8), pady=14, sticky="ew"
        )

        self.status_menu = ctk.CTkOptionMenu(
            filters,
            values=["All", "Available", "Pending", "Adopted"],
            width=140,
            height=40,
            corner_radius=13,
            fg_color=COLORS["secondary_soft"],
            button_color=COLORS["secondary"],
            button_hover_color="#A994D9",
            text_color=COLORS["text"],
        )
        self.status_menu.grid(row=0, column=1, padx=8, pady=14)

        cute_button(
            filters,
            "Search",
            command=self.refresh,
            width=95,
        ).grid(row=0, column=2, padx=(8, 16), pady=14)

        self.pet_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.pet_scroll.grid(row=2, column=0, sticky="nsew")
        self.pet_scroll.grid_columnconfigure((0, 1, 2), weight=1)

    def refresh(self):
        clear_children(self.pet_scroll)

        rows = list_pets(
            self.search_entry.get() if hasattr(self, "search_entry") else "",
            self.status_menu.get() if hasattr(self, "status_menu") else "All",
        )

        if not rows:
            empty = make_card(self.pet_scroll)
            empty.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10)
            ctk.CTkLabel(
                empty,
                text="🐶\nNo pets found\nTry another search, bestie ♡",
                font=ctk.CTkFont(size=15),
                text_color=COLORS["muted"],
                justify="center",
            ).pack(pady=50)
            return

        for index, pet in enumerate(rows):
            self._pet_card(pet, index // 3, index % 3)

    def _pet_card(self, pet, row, col):
        card = make_card(self.pet_scroll)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        image = load_pet_image(pet["photo"], size=(220, 145))
        if image:
            label = ctk.CTkLabel(card, text="", image=image)
            label.image = image
        else:
            label = ctk.CTkLabel(
                card,
                text="🐾",
                height=145,
                fg_color=COLORS["primary_soft"],
                corner_radius=16,
                font=ctk.CTkFont(size=48),
            )
        label.pack(fill="x", padx=14, pady=(14, 10))

        title_row = ctk.CTkFrame(card, fg_color="transparent")
        title_row.pack(fill="x", padx=16)

        ctk.CTkLabel(
            title_row,
            text=pet["name"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        status_pill(title_row, pet["status"]).pack(side="right")

        ctk.CTkLabel(
            card,
            text=f"{pet['species']} • {pet['breed']}\n{pet['age']:g} yrs • {pet['sex']}",
            justify="left",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(5, 10))

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=14, pady=(0, 14))

        cute_button(
            buttons,
            "Edit",
            command=lambda pet_id=pet["id"]: self.open_edit_pet(pet_id),
            secondary=True,
            width=90,
        ).pack(side="left", padx=(0, 6))

        if pet["status"] != "Adopted":
            cute_button(
                buttons,
                "Apply",
                command=lambda pet_id=pet["id"]: self.open_application(pet_id),
                width=90,
            ).pack(side="right")

    def open_add_pet(self):
        PetFormWindow(self, on_saved=self._after_save)

    def open_edit_pet(self, pet_id):
        PetFormWindow(self, pet=get_pet(pet_id), on_saved=self._after_save)

    def open_application(self, pet_id):
        ApplicationFormWindow(self, pet=get_pet(pet_id), on_saved=self._after_save)

    def _after_save(self):
        self.refresh()
        self.app.refresh_all()


class PetFormWindow(ctk.CTkToplevel):
    def __init__(self, parent, pet=None, on_saved=None):
        super().__init__(parent)
        self.pet = pet
        self.on_saved = on_saved
        self.photo_path = pet["photo"] if pet else None

        self.title("Edit Pet" if pet else "Add New Pet")
        self.geometry("620x700")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["background"])
        self.grab_set()

        card = make_card(self)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        ctk.CTkLabel(
            card,
            text="🌸  " + ("Edit Pet Profile" if pet else "Add a New Cutie"),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(anchor="w", padx=24, pady=(24, 4))

        ctk.CTkLabel(
            card,
            text="Fill in the pet details below.",
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=24, pady=(0, 18))

        self.name = self._entry(card, "Pet Name", pet["name"] if pet else "")
        self.species = self._entry(card, "Species", pet["species"] if pet else "")
        self.breed = self._entry(card, "Breed", pet["breed"] if pet else "")
        self.age = self._entry(card, "Age in Years", str(pet["age"]) if pet else "")

        self.sex = ctk.CTkOptionMenu(
            card,
            values=["Male", "Female"],
            height=38,
            corner_radius=12,
            fg_color=COLORS["secondary_soft"],
            button_color=COLORS["secondary"],
            text_color=COLORS["text"],
        )
        self.sex.set(pet["sex"] if pet else "Female")
        self._labeled_widget(card, "Sex", self.sex)

        if pet:
            self.status = ctk.CTkOptionMenu(
                card,
                values=["Available", "Pending", "Adopted"],
                height=38,
                corner_radius=12,
                fg_color=COLORS["secondary_soft"],
                button_color=COLORS["secondary"],
                text_color=COLORS["text"],
            )
            self.status.set(pet["status"])
            self._labeled_widget(card, "Status", self.status)

        ctk.CTkLabel(
            card,
            text="Description",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(10, 5))

        self.description = ctk.CTkTextbox(
            card,
            height=90,
            corner_radius=12,
            border_width=1,
            border_color=COLORS["line"],
        )
        self.description.pack(fill="x", padx=24)
        if pet and pet["description"]:
            self.description.insert("1.0", pet["description"])

        photo_row = ctk.CTkFrame(card, fg_color="transparent")
        photo_row.pack(fill="x", padx=24, pady=14)

        cute_button(
            photo_row,
            "📷 Choose Photo",
            command=self.choose_photo,
            secondary=True,
            width=135,
        ).pack(side="left")

        self.photo_label = ctk.CTkLabel(
            photo_row,
            text="No photo selected" if not self.photo_path else Path(self.photo_path).name,
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11),
        )
        self.photo_label.pack(side="left", padx=10)

        cute_button(
            card,
            "Save Pet ♡",
            command=self.save,
            width=150,
        ).pack(pady=(8, 22))

    def _entry(self, parent, label, value):
        ctk.CTkLabel(
            parent,
            text=label,
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(8, 5))

        entry = ctk.CTkEntry(
            parent,
            height=38,
            corner_radius=12,
            border_color=COLORS["line"],
        )
        entry.pack(fill="x", padx=24)
        if value:
            entry.insert(0, value)
        return entry

    def _labeled_widget(self, parent, label, widget):
        ctk.CTkLabel(
            parent,
            text=label,
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(8, 5))
        widget.pack(fill="x", padx=24)

    def choose_photo(self):
        path = filedialog.askopenfilename(
            title="Choose a pet photo",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.webp"),
            ],
        )
        if path:
            self.photo_path = path
            self.photo_label.configure(text=Path(path).name)

    def save(self):
        name = self.name.get().strip()
        species = self.species.get().strip()
        breed = self.breed.get().strip()
        age_text = self.age.get().strip()
        sex = self.sex.get()
        description = self.description.get("1.0", "end").strip()

        if not name or not species or not breed or not age_text:
            messagebox.showerror("Missing Details", "Please fill in all required fields.")
            return

        try:
            age = float(age_text)
        except ValueError:
            messagebox.showerror("Invalid Age", "Age must be a number.")
            return

        if age < 0 or age > 50:
            messagebox.showerror("Invalid Age", "Age must be between 0 and 50.")
            return

        photo = self.pet["photo"] if self.pet else None

        if self.photo_path and self.photo_path != photo:
            try:
                photo = copy_photo(self.photo_path)
            except ValueError as exc:
                messagebox.showerror("Photo Error", str(exc))
                return

        if self.pet:
            update_pet(
                self.pet["id"], name, species, breed, age, sex,
                description, self.status.get(), photo
            )
        else:
            add_pet(name, species, breed, age, sex, description, photo)

        messagebox.showinfo("Saved ♡", f"{name}'s profile was saved successfully!")
        if self.on_saved:
            self.on_saved()
        self.destroy()


class ApplicationFormWindow(ctk.CTkToplevel):
    def __init__(self, parent, pet, on_saved=None):
        super().__init__(parent)
        self.pet = pet
        self.on_saved = on_saved

        self.title(f"Apply to Adopt {pet['name']}")
        self.geometry("620x650")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["background"])
        self.grab_set()

        card = make_card(self)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        ctk.CTkLabel(
            card,
            text=f"💗  Apply to adopt {pet['name']}",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(anchor="w", padx=24, pady=(24, 4))

        ctk.CTkLabel(
            card,
            text=f"{pet['species']} • {pet['breed']} • {pet['age']:g} years old",
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=24, pady=(0, 16))

        self.name = self._entry(card, "Full Name")
        self.email = self._entry(card, "Email")
        self.contact = self._entry(card, "Contact Number")
        self.address = self._entry(card, "Home Address")

        ctk.CTkLabel(
            card,
            text="Why do you want to adopt this pet?",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(10, 5))

        self.reason = ctk.CTkTextbox(
            card,
            height=100,
            corner_radius=12,
            border_width=1,
            border_color=COLORS["line"],
        )
        self.reason.pack(fill="x", padx=24)

        cute_button(
            card,
            "Submit Application 💌",
            command=self.submit,
            width=180,
        ).pack(pady=20)

    def _entry(self, parent, label):
        ctk.CTkLabel(
            parent,
            text=label,
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(8, 5))

        entry = ctk.CTkEntry(
            parent,
            height=38,
            corner_radius=12,
            border_color=COLORS["line"],
        )
        entry.pack(fill="x", padx=24)
        return entry

    def submit(self):
        full_name = self.name.get().strip()
        email = self.email.get().strip()
        contact = self.contact.get().strip()
        address = self.address.get().strip()
        reason = self.reason.get("1.0", "end").strip()

        if not all([full_name, email, contact, address, reason]):
            messagebox.showerror("Missing Details", "Please complete the whole form.")
            return

        if not validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if not validate_contact(contact):
            messagebox.showerror("Invalid Contact", "Please enter a valid contact number.")
            return

        try:
            create_application(
                self.pet["id"], full_name, email, contact, address, reason
            )
        except ValueError as exc:
            messagebox.showerror("Application Error", str(exc))
            return

        messagebox.showinfo(
            "Application Sent 💌",
            f"Application for {self.pet['name']} was submitted successfully!"
        )
        if self.on_saved:
            self.on_saved()
        self.destroy()
