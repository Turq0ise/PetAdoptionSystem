import customtkinter as ctk

from database import adoption_history
from ui.theme import COLORS
from ui.components import page_title, make_card, clear_children


class HistoryPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = page_title(
            self,
            "Adoption history",
            "Forever homes 🌸",
            "A sweet little record of completed adoptions.",
        )
        title.grid(row=0, column=0, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.scroll.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        self.scroll.grid_columnconfigure(0, weight=1)

    def refresh(self):
        clear_children(self.scroll)
        rows = adoption_history()

        if not rows:
            card = make_card(self.scroll)
            card.grid(row=0, column=0, sticky="ew", pady=8)
            ctk.CTkLabel(
                card,
                text="🏠\nNo completed adoptions yet\nTheir forever-home stories will appear here ♡",
                text_color=COLORS["muted"],
                justify="center",
                font=ctk.CTkFont(size=14),
            ).pack(pady=55)
            return

        for idx, row in enumerate(rows):
            card = make_card(self.scroll)
            card.grid(row=idx, column=0, sticky="ew", pady=7)
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                card,
                text="🌷",
                width=54,
                font=ctk.CTkFont(size=26),
            ).grid(row=0, column=0, rowspan=2, padx=(16, 4), pady=15)

            ctk.CTkLabel(
                card,
                text=f"{row['pet_name']} found a forever home!",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=COLORS["text"],
            ).grid(row=0, column=1, sticky="sw", pady=(15, 2))

            ctk.CTkLabel(
                card,
                text=f"Adopted by {row['full_name']}  •  {row['adoption_date']}",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["muted"],
            ).grid(row=1, column=1, sticky="nw", pady=(0, 14))

            ctk.CTkLabel(
                card,
                text=f"#{row['id']}",
                fg_color=COLORS["secondary_soft"],
                text_color="#6B56A3",
                corner_radius=999,
                width=54,
                height=28,
                font=ctk.CTkFont(size=11, weight="bold"),
            ).grid(row=0, column=2, rowspan=2, padx=16)
