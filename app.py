import customtkinter as ctk

from database import init_db
from ui.dashboard import DashboardPage
from ui.pets import PetsPage
from ui.applications import ApplicationsPage
from ui.history import HistoryPage
from ui.theme import COLORS


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class PetAdoptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        init_db()

        self.title("PawMatch — Pet Adoption Management System")
        self.geometry("1280x760")
        self.minsize(1100, 680)
        self.configure(fg_color=COLORS["background"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=COLORS["sidebar"],
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        logo = ctk.CTkLabel(
            self.sidebar,
            text="🐾  PawMatch",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLORS["primary_dark"],
        )
        logo.grid(row=0, column=0, padx=22, pady=(28, 4), sticky="w")

        tagline = ctk.CTkLabel(
            self.sidebar,
            text="find a home, share a heart ♡",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        )
        tagline.grid(row=1, column=0, padx=22, pady=(0, 26), sticky="w")

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "🏠"),
            ("Pets", "🐶"),
            ("Applications", "💌"),
            ("History", "🌸"),
        ]

        for idx, (name, icon) in enumerate(nav_items, start=2):
            button = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}   {name}",
                anchor="w",
                height=44,
                corner_radius=14,
                fg_color="transparent",
                hover_color=COLORS["hover"],
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda page=name: self.show_page(page),
            )
            button.grid(row=idx, column=0, padx=16, pady=5, sticky="ew")
            self.nav_buttons[name] = button

        footer = ctk.CTkLabel(
            self.sidebar,
            text="Made with love for happy tails ♡",
            wraplength=170,
            justify="left",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["muted"],
        )
        footer.grid(row=8, column=0, padx=22, pady=22, sticky="sw")

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=0,
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.pages = {}
        self.show_page("Dashboard")

    def show_page(self, name):
        for page in self.pages.values():
            page.grid_forget()

        if name not in self.pages:
            page_class = {
                "Dashboard": DashboardPage,
                "Pets": PetsPage,
                "Applications": ApplicationsPage,
                "History": HistoryPage,
            }[name]
            self.pages[name] = page_class(self.content, app=self)

        page = self.pages[name]
        page.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)

        if hasattr(page, "refresh"):
            page.refresh()

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

    def refresh_all(self):
        for page in self.pages.values():
            if hasattr(page, "refresh"):
                page.refresh()


if __name__ == "__main__":
    app = PetAdoptionApp()
    app.mainloop()
