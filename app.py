import re
import customtkinter as ctk
from tkinter import messagebox

from database import DatabaseManager


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


COLORS = {
    "background": "#FFF8FB",
    "sidebar": "#FFF0F6",
    "card": "#FFFFFF",
    "primary": "#E77EAE",
    "primary_dark": "#A64E77",
    "primary_soft": "#F9D9E8",
    "lavender": "#B79DE8",
    "lavender_soft": "#EEE7FA",
    "mint": "#BCE8D5",
    "mint_dark": "#3F8166",
    "yellow": "#F7DFA3",
    "text": "#493E45",
    "muted": "#8B7D86",
    "line": "#F0DCE7",
    "danger": "#E17878",
    "danger_soft": "#FBE5E5",
}


def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()


def make_card(parent):
    return ctk.CTkFrame(
        parent,
        fg_color=COLORS["card"],
        corner_radius=20,
        border_width=1,
        border_color=COLORS["line"],
    )


class PetAdoptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Uses the user's DatabaseManager exactly as provided.
        self.db = DatabaseManager()

        self.title("PawMatch — Pet Adoption Management System")
        self.geometry("1280x760")
        self.minsize(1050, 650)
        self.configure(fg_color=COLORS["background"])

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=COLORS["sidebar"],
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="🐾  PawMatch",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(anchor="w", padx=22, pady=(28, 3))

        ctk.CTkLabel(
            self.sidebar,
            text="find a home, share a heart ♡",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=22, pady=(0, 26))

        self.nav_buttons = {}
        for name, icon in [
            ("Dashboard", "🏠"),
            ("Pets", "🐶"),
            ("Adoptions", "💗"),
        ]:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}   {name}",
                anchor="w",
                height=44,
                corner_radius=14,
                fg_color="transparent",
                hover_color=COLORS["primary_soft"],
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda page=name: self.show_page(page),
            )
            btn.pack(fill="x", padx=16, pady=5)
            self.nav_buttons[name] = btn

        ctk.CTkLabel(
            self.sidebar,
            text="Made with love for happy tails ♡",
            wraplength=170,
            justify="left",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["muted"],
        ).pack(side="bottom", anchor="w", padx=22, pady=22)

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=0,
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.show_page("Dashboard")

    # ------------------------------------------------------------------
    # DATABASE HELPERS
    # ------------------------------------------------------------------

    def query_one(self, sql, params=()):
        self.db.cursor.execute(sql, params)
        return self.db.cursor.fetchone()

    def query_all(self, sql, params=()):
        self.db.cursor.execute(sql, params)
        return self.db.cursor.fetchall()

    def refresh_current(self):
        page = getattr(self, "current_page", "Dashboard")
        self.show_page(page)

    # ------------------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------------------

    def show_page(self, name):
        self.current_page = name
        clear_frame(self.content)

        for button_name, button in self.nav_buttons.items():
            if button_name == name:
                button.configure(
                    fg_color=COLORS["primary_soft"],
                    text_color=COLORS["primary_dark"],
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=COLORS["text"],
                )

        if name == "Dashboard":
            self.build_dashboard()
        elif name == "Pets":
            self.build_pets()
        else:
            self.build_adoptions()

    # ------------------------------------------------------------------
    # SHARED UI
    # ------------------------------------------------------------------

    def page_header(self, parent, eyebrow, title, subtitle):
        ctk.CTkLabel(
            parent,
            text=eyebrow.upper(),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(3, 0))

        ctk.CTkLabel(
            parent,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=COLORS["muted"],
        ).pack(anchor="w", pady=(1, 0))

    def status_pill(self, parent, status):
        if status == "Available":
            bg, fg = COLORS["mint"], COLORS["mint_dark"]
        else:
            bg, fg = COLORS["lavender_soft"], "#6C55A5"

        return ctk.CTkLabel(
            parent,
            text=f"  {status}  ",
            fg_color=bg,
            text_color=fg,
            corner_radius=999,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
        )

    # ------------------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------------------

    def build_dashboard(self):
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        wrapper.grid_columnconfigure((0, 1, 2), weight=1)
        wrapper.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(wrapper, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")
        self.page_header(
            title_box,
            "Welcome back",
            "Happy tails start here ♡",
            "Manage pets and completed adoptions using your SQLite database.",
        )

        ctk.CTkButton(
            header,
            text="+ Add Pet",
            width=125,
            height=42,
            corner_radius=14,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.open_add_pet,
        ).grid(row=0, column=1, sticky="e")

        total = self.query_one("SELECT COUNT(*) FROM pets")[0]
        available = self.query_one(
            "SELECT COUNT(*) FROM pets WHERE status='Available'"
        )[0]
        adopted = self.query_one(
            "SELECT COUNT(*) FROM pets WHERE status='Adopted'"
        )[0]

        stats = [
            ("🐾", "Total Pets", total, COLORS["primary_soft"]),
            ("🌿", "Available", available, COLORS["mint"]),
            ("🌸", "Adopted", adopted, COLORS["lavender_soft"]),
        ]

        for i, (icon, label, value, color) in enumerate(stats):
            card = make_card(wrapper)
            card.grid(row=1, column=i, padx=7, pady=(22, 18), sticky="ew")
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                card,
                text=icon,
                width=48,
                height=48,
                fg_color=color,
                corner_radius=15,
                font=ctk.CTkFont(size=22),
            ).grid(row=0, column=0, rowspan=2, padx=15, pady=17)

            ctk.CTkLabel(
                card,
                text=label,
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=12, weight="bold"),
            ).grid(row=0, column=1, sticky="sw", pady=(15, 0))

            ctk.CTkLabel(
                card,
                text=str(value),
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=29, weight="bold"),
            ).grid(row=1, column=1, sticky="nw", pady=(0, 14))

        recent_card = make_card(wrapper)
        recent_card.grid(row=2, column=0, columnspan=3, sticky="nsew")

        ctk.CTkLabel(
            recent_card,
            text="Recent adoptions 💗",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", padx=22, pady=(20, 2))

        ctk.CTkLabel(
            recent_card,
            text="The newest pets who found their forever homes.",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=22, pady=(0, 12))

        rows = self.query_all(
            """
            SELECT a.adoption_id, a.adopter_name, a.contact_number,
                   p.name, p.species, p.breed
            FROM adoptions a
            JOIN pets p ON p.pet_id = a.pet_id
            ORDER BY a.adoption_id DESC
            LIMIT 6
            """
        )

        if not rows:
            ctk.CTkLabel(
                recent_card,
                text="No adoptions yet. Their forever-home stories will appear here ♡",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=13),
            ).pack(pady=38)
        else:
            for adoption_id, adopter, contact, pet_name, species, breed in rows:
                row = ctk.CTkFrame(
                    recent_card,
                    fg_color="#FFF9FC",
                    corner_radius=13,
                )
                row.pack(fill="x", padx=20, pady=4)

                ctk.CTkLabel(
                    row,
                    text="🌷",
                    width=40,
                    font=ctk.CTkFont(size=19),
                ).pack(side="left", padx=(10, 2), pady=10)

                info = ctk.CTkFrame(row, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, pady=8)

                ctk.CTkLabel(
                    info,
                    text=f"{pet_name} was adopted by {adopter}",
                    anchor="w",
                    text_color=COLORS["text"],
                    font=ctk.CTkFont(size=13, weight="bold"),
                ).pack(fill="x")

                ctk.CTkLabel(
                    info,
                    text=f"{species} • {breed}   |   {contact}",
                    anchor="w",
                    text_color=COLORS["muted"],
                    font=ctk.CTkFont(size=11),
                ).pack(fill="x")

                ctk.CTkLabel(
                    row,
                    text=f"#{adoption_id}",
                    width=55,
                    height=27,
                    corner_radius=999,
                    fg_color=COLORS["lavender_soft"],
                    text_color="#6C55A5",
                    font=ctk.CTkFont(size=11, weight="bold"),
                ).pack(side="right", padx=14)

    # ------------------------------------------------------------------
    # PETS PAGE
    # ------------------------------------------------------------------

    def build_pets(self):
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(wrapper, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")
        self.page_header(
            title_box,
            "Pet management",
            "Meet the cuties 🐾",
            "Search the pets stored in your existing database.",
        )

        ctk.CTkButton(
            header,
            text="+ Add Pet",
            width=125,
            height=42,
            corner_radius=14,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.open_add_pet,
        ).grid(row=0, column=1, sticky="e")

        filter_card = make_card(wrapper)
        filter_card.grid(row=1, column=0, sticky="ew", pady=(18, 14))
        filter_card.grid_columnconfigure(0, weight=1)

        self.pet_search = ctk.CTkEntry(
            filter_card,
            placeholder_text="Search name, species, or breed...",
            height=42,
            corner_radius=13,
            border_color=COLORS["line"],
        )
        self.pet_search.grid(
            row=0, column=0, padx=(16, 8), pady=14, sticky="ew"
        )
        self.pet_search.bind("<Return>", lambda event: self.load_pet_cards())

        self.pet_status = ctk.CTkOptionMenu(
            filter_card,
            values=["All", "Available", "Adopted"],
            width=150,
            height=42,
            corner_radius=13,
            fg_color=COLORS["lavender_soft"],
            button_color=COLORS["lavender"],
            button_hover_color="#A88CD8",
            text_color=COLORS["text"],
            command=lambda _: self.load_pet_cards(),
        )
        self.pet_status.grid(row=0, column=1, padx=8, pady=14)

        ctk.CTkButton(
            filter_card,
            text="Search",
            width=105,
            height=42,
            corner_radius=13,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.load_pet_cards,
        ).grid(row=0, column=2, padx=(8, 16), pady=14)

        self.pet_scroll = ctk.CTkScrollableFrame(
            wrapper,
            fg_color="transparent",
            corner_radius=0,
        )
        self.pet_scroll.grid(row=2, column=0, sticky="nsew")
        self.pet_scroll.grid_columnconfigure((0, 1, 2), weight=1)

        self.load_pet_cards()

    def load_pet_cards(self):
        clear_frame(self.pet_scroll)

        keyword = self.pet_search.get().strip()
        status = self.pet_status.get()

        sql = """
            SELECT pet_id, name, species, breed, age, status
            FROM pets
            WHERE 1=1
        """
        params = []

        if keyword:
            like = f"%{keyword}%"
            sql += " AND (name LIKE ? OR species LIKE ? OR breed LIKE ?)"
            params.extend([like, like, like])

        if status != "All":
            sql += " AND status = ?"
            params.append(status)

        sql += " ORDER BY pet_id DESC"

        rows = self.query_all(sql, params)

        if not rows:
            empty = make_card(self.pet_scroll)
            empty.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10)
            ctk.CTkLabel(
                empty,
                text="🐶\nNo matching pets found\nTry another search ♡",
                justify="center",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=14),
            ).pack(pady=50)
            return

        for index, pet in enumerate(rows):
            self.pet_card(pet, index // 3, index % 3)

    def pet_card(self, pet, row, col):
        pet_id, name, species, breed, age, status = pet

        card = make_card(self.pet_scroll)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        emoji = "🐶" if species.lower() == "dog" else "🐱" if species.lower() == "cat" else "🐾"

        ctk.CTkLabel(
            card,
            text=emoji,
            height=135,
            fg_color=COLORS["primary_soft"],
            corner_radius=16,
            font=ctk.CTkFont(size=52),
        ).pack(fill="x", padx=14, pady=(14, 10))

        title_row = ctk.CTkFrame(card, fg_color="transparent")
        title_row.pack(fill="x", padx=16)

        ctk.CTkLabel(
            title_row,
            text=name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        self.status_pill(title_row, status).pack(side="right")

        ctk.CTkLabel(
            card,
            text=f"{species} • {breed}\n{age} yrs",
            justify="left",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(5, 12))

        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=14, pady=(0, 14))

        ctk.CTkButton(
            actions,
            text="Edit",
            width=90,
            height=38,
            corner_radius=13,
            fg_color=COLORS["lavender_soft"],
            hover_color="#E3D8F8",
            text_color="#6C55A5",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda pid=pet_id: self.open_edit_pet(pid),
        ).pack(side="left")

        if status == "Available":
            ctk.CTkButton(
                actions,
                text="Adopt",
                width=95,
                height=38,
                corner_radius=13,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                font=ctk.CTkFont(size=13, weight="bold"),
                command=lambda pid=pet_id: self.open_adoption(pid),
            ).pack(side="right")

    # ------------------------------------------------------------------
    # ADD / EDIT PET
    # ------------------------------------------------------------------

    def open_add_pet(self):
        self.pet_form()

    def open_edit_pet(self, pet_id):
        pet = self.query_one(
            """
            SELECT pet_id, name, species, breed, age, status
            FROM pets
            WHERE pet_id=?
            """,
            (pet_id,),
        )
        if pet:
            self.pet_form(pet)

    def pet_form(self, pet=None):
        window = ctk.CTkToplevel(self)
        window.title("Edit Pet" if pet else "Add New Pet")
        window.geometry("620x620")
        window.minsize(560, 560)
        window.configure(fg_color=COLORS["background"])
        window.grab_set()

        # Scrollable content + fixed footer keeps Confirm visible.
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(
            window,
            fg_color=COLORS["background"],
            corner_radius=0,
        )
        scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        card = make_card(scroll)
        card.pack(fill="x", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            card,
            text="🌸  " + ("Edit Pet" if pet else "Add a New Cutie"),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(anchor="w", padx=24, pady=(24, 3))

        ctk.CTkLabel(
            card,
            text="Fill in the pet details below.",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=24, pady=(0, 18))

        def field(label, value=""):
            ctk.CTkLabel(
                card,
                text=label,
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(anchor="w", padx=24, pady=(8, 5))

            entry = ctk.CTkEntry(
                card,
                height=40,
                corner_radius=12,
                border_color=COLORS["line"],
            )
            entry.pack(fill="x", padx=24)

            if value != "":
                entry.insert(0, str(value))

            return entry

        name_entry = field("Pet Name *", pet[1] if pet else "")
        species_entry = field("Species *", pet[2] if pet else "")
        breed_entry = field("Breed *", pet[3] if pet else "")
        age_entry = field("Age in Years *", pet[4] if pet else "")

        status_menu = None
        if pet:
            ctk.CTkLabel(
                card,
                text="Status *",
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(anchor="w", padx=24, pady=(8, 5))

            status_menu = ctk.CTkOptionMenu(
                card,
                values=["Available", "Adopted"],
                height=40,
                corner_radius=12,
                fg_color=COLORS["lavender_soft"],
                button_color=COLORS["lavender"],
                text_color=COLORS["text"],
            )
            status_menu.set(pet[5])
            status_menu.pack(fill="x", padx=24, pady=(0, 24))
        else:
            ctk.CTkLabel(
                card,
                text="New pets are automatically marked Available ♡",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=11),
            ).pack(anchor="w", padx=24, pady=(14, 24))

        footer = ctk.CTkFrame(
            window,
            fg_color=COLORS["card"],
            corner_radius=0,
            border_width=1,
            border_color=COLORS["line"],
        )
        footer.grid(row=1, column=0, sticky="ew")
        footer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            footer,
            text="♡ Check the details before saving.",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11),
        ).grid(row=0, column=0, padx=20, pady=17, sticky="w")

        ctk.CTkButton(
            footer,
            text="Cancel",
            width=90,
            height=38,
            corner_radius=13,
            fg_color=COLORS["lavender_soft"],
            hover_color="#E3D8F8",
            text_color="#6C55A5",
            command=window.destroy,
        ).grid(row=0, column=1, padx=(6, 5), pady=16)

        def save_pet():
            name = name_entry.get().strip()
            species = species_entry.get().strip()
            breed = breed_entry.get().strip()
            age_text = age_entry.get().strip()

            if not name or not species or not breed or not age_text:
                messagebox.showerror(
                    "Missing Details",
                    "Please complete Pet Name, Species, Breed, and Age.",
                    parent=window,
                )
                return

            try:
                age = int(age_text)
            except ValueError:
                messagebox.showerror(
                    "Invalid Age",
                    "Age must be a whole number.",
                    parent=window,
                )
                return

            if age < 0:
                messagebox.showerror(
                    "Invalid Age",
                    "Age cannot be negative.",
                    parent=window,
                )
                return

            if pet:
                new_status = status_menu.get()

                # If manually changed back to Available, remove its adoption
                # record so the two-table database stays consistent.
                if pet[5] == "Adopted" and new_status == "Available":
                    self.db.cursor.execute(
                        "DELETE FROM adoptions WHERE pet_id=?",
                        (pet[0],),
                    )

                self.db.cursor.execute(
                    """
                    UPDATE pets
                    SET name=?, species=?, breed=?, age=?, status=?
                    WHERE pet_id=?
                    """,
                    (name, species, breed, age, new_status, pet[0]),
                )
                success = f"{name}'s profile was updated!"
            else:
                self.db.cursor.execute(
                    """
                    INSERT INTO pets (name, species, breed, age, status)
                    VALUES (?, ?, ?, ?, 'Available')
                    """,
                    (name, species, breed, age),
                )
                success = f"{name} was added successfully!"

            self.db.conn.commit()
            messagebox.showinfo("Saved ♡", success, parent=window)
            window.destroy()
            self.refresh_current()

        ctk.CTkButton(
            footer,
            text="Confirm Changes ♡" if pet else "Confirm & Add Pet ♡",
            width=165,
            height=38,
            corner_radius=13,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=save_pet,
        ).grid(row=0, column=2, padx=(5, 20), pady=16)

        window.bind("<Return>", lambda event: save_pet())
        window.after(100, name_entry.focus_set)

    # ------------------------------------------------------------------
    # ADOPT PET
    # ------------------------------------------------------------------

    def open_adoption(self, pet_id):
        pet = self.query_one(
            """
            SELECT pet_id, name, species, breed, age, status
            FROM pets
            WHERE pet_id=?
            """,
            (pet_id,),
        )

        if not pet:
            messagebox.showerror("Pet Not Found", "The selected pet no longer exists.")
            return

        if pet[5] != "Available":
            messagebox.showerror(
                "Not Available",
                "This pet has already been adopted.",
            )
            return

        window = ctk.CTkToplevel(self)
        window.title(f"Adopt {pet[1]}")
        window.geometry("560x480")
        window.resizable(False, False)
        window.configure(fg_color=COLORS["background"])
        window.grab_set()

        card = make_card(window)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        ctk.CTkLabel(
            card,
            text=f"💗  Adopt {pet[1]}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(anchor="w", padx=24, pady=(24, 3))

        ctk.CTkLabel(
            card,
            text=f"{pet[2]} • {pet[3]} • {pet[4]} yrs",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=24, pady=(0, 18))

        def field(label, placeholder=""):
            ctk.CTkLabel(
                card,
                text=label,
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(anchor="w", padx=24, pady=(10, 5))

            entry = ctk.CTkEntry(
                card,
                height=40,
                corner_radius=12,
                border_color=COLORS["line"],
                placeholder_text=placeholder,
            )
            entry.pack(fill="x", padx=24)
            return entry

        adopter_entry = field("Adopter's Full Name *")
        contact_entry = field("Contact Number *", "09XXXXXXXXX")

        ctk.CTkLabel(
            card,
            text="Your database records the adoption immediately after confirmation.",
            wraplength=460,
            justify="left",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11),
        ).pack(anchor="w", padx=24, pady=(16, 12))

        def confirm_adoption():
            adopter = adopter_entry.get().strip()
            contact = contact_entry.get().strip()

            if not adopter:
                messagebox.showerror(
                    "Missing Name",
                    "Please enter the adopter's full name.",
                    parent=window,
                )
                return

            if not re.fullmatch(r"09\d{9}", contact):
                messagebox.showerror(
                    "Invalid Contact",
                    "Contact number must be 11 digits and start with 09.",
                    parent=window,
                )
                return

            current = self.query_one(
                "SELECT status FROM pets WHERE pet_id=?",
                (pet_id,),
            )
            if not current or current[0] != "Available":
                messagebox.showerror(
                    "Not Available",
                    "This pet is no longer available.",
                    parent=window,
                )
                return

            self.db.cursor.execute(
                """
                INSERT INTO adoptions
                (pet_id, adopter_name, contact_number)
                VALUES (?, ?, ?)
                """,
                (pet_id, adopter, contact),
            )
            self.db.cursor.execute(
                """
                UPDATE pets
                SET status='Adopted'
                WHERE pet_id=?
                """,
                (pet_id,),
            )
            self.db.conn.commit()

            messagebox.showinfo(
                "Adoption Complete 🌸",
                f"{pet[1]} has been adopted by {adopter}!",
                parent=window,
            )
            window.destroy()
            self.refresh_current()

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(14, 22))

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=100,
            height=40,
            corner_radius=13,
            fg_color=COLORS["lavender_soft"],
            hover_color="#E3D8F8",
            text_color="#6C55A5",
            command=window.destroy,
        ).pack(side="left")

        ctk.CTkButton(
            buttons,
            text="Confirm Adoption ♡",
            width=165,
            height=40,
            corner_radius=13,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=confirm_adoption,
        ).pack(side="right")

    # ------------------------------------------------------------------
    # ADOPTION HISTORY PAGE
    # ------------------------------------------------------------------

    def build_adoptions(self):
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(1, weight=1)

        title_box = ctk.CTkFrame(wrapper, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")
        self.page_header(
            title_box,
            "Adoption history",
            "Forever homes 🌸",
            "Completed adoptions stored in your adoptions table.",
        )

        scroll = ctk.CTkScrollableFrame(
            wrapper,
            fg_color="transparent",
            corner_radius=0,
        )
        scroll.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        scroll.grid_columnconfigure(0, weight=1)

        rows = self.query_all(
            """
            SELECT a.adoption_id, a.adopter_name, a.contact_number,
                   p.pet_id, p.name, p.species, p.breed, p.age
            FROM adoptions a
            JOIN pets p ON p.pet_id = a.pet_id
            ORDER BY a.adoption_id DESC
            """
        )

        if not rows:
            empty = make_card(scroll)
            empty.grid(row=0, column=0, sticky="ew", pady=8)
            ctk.CTkLabel(
                empty,
                text="🏠\nNo completed adoptions yet\nForever-home stories will appear here ♡",
                text_color=COLORS["muted"],
                justify="center",
                font=ctk.CTkFont(size=14),
            ).pack(pady=55)
            return

        for i, row in enumerate(rows):
            (
                adoption_id,
                adopter,
                contact,
                pet_id,
                pet_name,
                species,
                breed,
                age,
            ) = row

            card = make_card(scroll)
            card.grid(row=i, column=0, sticky="ew", pady=7)
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                card,
                text="🌷",
                width=55,
                font=ctk.CTkFont(size=26),
            ).grid(row=0, column=0, rowspan=2, padx=(16, 4), pady=15)

            ctk.CTkLabel(
                card,
                text=f"{pet_name} found a forever home!",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=COLORS["text"],
            ).grid(row=0, column=1, sticky="sw", pady=(15, 2))

            ctk.CTkLabel(
                card,
                text=f"{species} • {breed} • {age} yrs   |   Adopted by {adopter} • {contact}",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["muted"],
            ).grid(row=1, column=1, sticky="nw", pady=(0, 14))

            ctk.CTkLabel(
                card,
                text=f"#{adoption_id}",
                fg_color=COLORS["lavender_soft"],
                text_color="#6C55A5",
                corner_radius=999,
                width=55,
                height=28,
                font=ctk.CTkFont(size=11, weight="bold"),
            ).grid(row=0, column=2, rowspan=2, padx=16)

    def on_close(self):
        try:
            self.db.close()
        finally:
            self.destroy()


if __name__ == "__main__":
    app = PetAdoptionApp()
    app.mainloop()
