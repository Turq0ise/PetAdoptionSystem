import customtkinter as ctk
from tkinter import messagebox

from database import (
    list_applications,
    get_application,
    approve_application,
    reject_application,
)
from ui.theme import COLORS
from ui.components import (
    page_title,
    make_card,
    status_pill,
    clear_children,
    cute_button,
)


class ApplicationsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        title = page_title(
            self,
            "Application management",
            "Little love letters 💌",
            "Review people who want to give your pets a forever home.",
        )
        title.grid(row=0, column=0, sticky="w")

        filters = make_card(self)
        filters.grid(row=1, column=0, sticky="ew", pady=(18, 14))
        filters.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Search applicant, email, or pet...",
            height=40,
            corner_radius=13,
            border_color=COLORS["line"],
        )
        self.search_entry.grid(
            row=0, column=0, padx=(16, 8), pady=14, sticky="ew"
        )

        self.status_menu = ctk.CTkOptionMenu(
            filters,
            values=["All", "Pending", "Approved", "Rejected"],
            width=140,
            height=40,
            corner_radius=13,
            fg_color=COLORS["secondary_soft"],
            button_color=COLORS["secondary"],
            text_color=COLORS["text"],
        )
        self.status_menu.grid(row=0, column=1, padx=8)

        cute_button(
            filters,
            "Search",
            command=self.refresh,
            width=95,
        ).grid(row=0, column=2, padx=(8, 16))

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.scroll.grid(row=2, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

    def refresh(self):
        clear_children(self.scroll)

        rows = list_applications(
            self.search_entry.get() if hasattr(self, "search_entry") else "",
            self.status_menu.get() if hasattr(self, "status_menu") else "All",
        )

        if not rows:
            card = make_card(self.scroll)
            card.grid(row=0, column=0, sticky="ew", pady=8)
            ctk.CTkLabel(
                card,
                text="💌\nNo applications found\nThe inbox is quiet right now ♡",
                justify="center",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=14),
            ).pack(pady=50)
            return

        for idx, row in enumerate(rows):
            card = make_card(self.scroll)
            card.grid(row=idx, column=0, sticky="ew", pady=7)
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                card,
                text="💗",
                width=50,
                font=ctk.CTkFont(size=24),
            ).grid(row=0, column=0, rowspan=2, padx=(16, 4), pady=15)

            ctk.CTkLabel(
                card,
                text=f"{row['full_name']}  →  {row['pet_name']}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=COLORS["text"],
            ).grid(row=0, column=1, sticky="sw", pady=(15, 2))

            ctk.CTkLabel(
                card,
                text=f"{row['email']}   •   {row['application_date']}",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["muted"],
            ).grid(row=1, column=1, sticky="nw", pady=(0, 14))

            status_pill(card, row["status"]).grid(
                row=0, column=2, rowspan=2, padx=10
            )

            cute_button(
                card,
                "Review",
                command=lambda app_id=row["id"]: self.open_review(app_id),
                secondary=True,
                width=90,
            ).grid(row=0, column=3, rowspan=2, padx=(4, 16))

    def open_review(self, application_id):
        ApplicationReviewWindow(
            self,
            application=get_application(application_id),
            on_changed=self._after_change,
        )

    def _after_change(self):
        self.refresh()
        self.app.refresh_all()


class ApplicationReviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, application, on_changed=None):
        super().__init__(parent)
        self.application = application
        self.on_changed = on_changed

        self.title(f"Application #{application['id']}")
        self.geometry("700x650")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["background"])
        self.grab_set()

        card = make_card(self)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            top,
            text=f"💌  Application #{application['id']}",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=COLORS["primary_dark"],
        ).pack(side="left")

        status_pill(top, application["status"]).pack(side="right")

        self._section(
            card,
            "Applicant",
            [
                ("Name", application["full_name"]),
                ("Email", application["email"]),
                ("Contact", application["contact"]),
                ("Address", application["address"]),
            ],
        )

        self._section(
            card,
            "Pet",
            [
                ("Name", application["pet_name"]),
                ("Breed", f"{application['species']} • {application['breed']}"),
                ("Age", f"{application['age']:g} years"),
                ("Sex", application["sex"]),
                ("Pet Status", application["pet_status"]),
            ],
        )

        reason_card = ctk.CTkFrame(
            card,
            fg_color="#FFF8FB",
            corner_radius=14,
        )
        reason_card.pack(fill="x", padx=24, pady=10)

        ctk.CTkLabel(
            reason_card,
            text="Why they want to adopt",
            text_color=COLORS["primary_dark"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=14, pady=(12, 3))

        ctk.CTkLabel(
            reason_card,
            text=application["reason"],
            wraplength=590,
            justify="left",
            text_color=COLORS["text"],
        ).pack(anchor="w", padx=14, pady=(0, 12))

        if application["status"] == "Pending":
            buttons = ctk.CTkFrame(card, fg_color="transparent")
            buttons.pack(fill="x", padx=24, pady=18)

            cute_button(
                buttons,
                "Reject",
                command=self.reject,
                danger=True,
                width=120,
            ).pack(side="left")

            cute_button(
                buttons,
                "Approve Adoption ♡",
                command=self.approve,
                width=170,
            ).pack(side="right")

    def _section(self, parent, title, rows):
        ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", padx=24, pady=(14, 5))

        box = ctk.CTkFrame(
            parent,
            fg_color="#FFF9FC",
            corner_radius=14,
        )
        box.pack(fill="x", padx=24)

        for label, value in rows:
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=5)

            ctk.CTkLabel(
                row,
                text=label,
                width=100,
                anchor="w",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=11),
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                anchor="w",
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(side="left", fill="x", expand=True)

    def approve(self):
        if not messagebox.askyesno(
            "Approve Adoption",
            "Approve this application and mark the pet as adopted?"
        ):
            return

        try:
            approve_application(self.application["id"])
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("Approved 🌸", "The adoption was approved successfully!")
        if self.on_changed:
            self.on_changed()
        self.destroy()

    def reject(self):
        if not messagebox.askyesno(
            "Reject Application",
            "Are you sure you want to reject this application?"
        ):
            return

        try:
            reject_application(self.application["id"])
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("Updated", "The application was rejected.")
        if self.on_changed:
            self.on_changed()
        self.destroy()
