import customtkinter as ctk

from database import dashboard_stats, recent_applications
from ui.theme import COLORS
from ui.components import page_title, make_card, status_pill, clear_children, cute_button


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(3, weight=1)

        header = page_title(
            self,
            "Welcome back",
            "Happy tails start here ♡",
            "A cozy little dashboard for your pet adoption records.",
        )
        header.grid(row=0, column=0, columnspan=3, sticky="w")

        cute_button(
            self,
            "＋ Add Pet",
            command=lambda: self.app.show_page("Pets"),
            width=130,
        ).grid(row=0, column=3, sticky="e")

        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(
            row=1, column=0, columnspan=4,
            sticky="ew", pady=(24, 18)
        )
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.recent_card = make_card(self)
        self.recent_card.grid(
            row=2, column=0, columnspan=4,
            sticky="nsew"
        )

        self.recent_inner = ctk.CTkFrame(
            self.recent_card,
            fg_color="transparent"
        )
        self.recent_inner.pack(fill="both", expand=True, padx=22, pady=20)

    def refresh(self):
        clear_children(self.stats_frame)
        clear_children(self.recent_inner)

        stats = dashboard_stats()
        cards = [
            ("🐾", "Total Pets", stats["total"], COLORS["primary_soft"]),
            ("🌿", "Available", stats["available"], COLORS["mint"]),
            ("💌", "Pending", stats["pending"], COLORS["yellow"]),
            ("🌸", "Adopted", stats["adopted"], COLORS["secondary_soft"]),
        ]

        for col, (icon, label, value, soft_color) in enumerate(cards):
            card = make_card(self.stats_frame)
            card.grid(row=0, column=col, padx=7, sticky="ew")
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                card,
                text=icon,
                width=44,
                height=44,
                fg_color=soft_color,
                corner_radius=14,
                font=ctk.CTkFont(size=20),
            ).grid(row=0, column=0, rowspan=2, padx=14, pady=16)

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
                font=ctk.CTkFont(size=28, weight="bold"),
            ).grid(row=1, column=1, sticky="nw", pady=(0, 14))

        ctk.CTkLabel(
            self.recent_inner,
            text="Recent adoption requests",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.recent_inner,
            text="The newest applications waiting in your little inbox 💗",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        ).pack(anchor="w", pady=(2, 14))

        rows = recent_applications()

        if not rows:
            ctk.CTkLabel(
                self.recent_inner,
                text="No applications yet. Your inbox is peaceful for now ♡",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=13),
            ).pack(pady=40)
            return

        for row in rows:
            item = ctk.CTkFrame(
                self.recent_inner,
                fg_color="#FFF9FC",
                corner_radius=14,
            )
            item.pack(fill="x", pady=5)

            ctk.CTkLabel(
                item,
                text="💌",
                width=36,
                font=ctk.CTkFont(size=18),
            ).pack(side="left", padx=(12, 4), pady=10)

            info = ctk.CTkFrame(item, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=9)

            ctk.CTkLabel(
                info,
                text=f"{row['full_name']} wants to adopt {row['pet_name']}",
                text_color=COLORS["text"],
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=row["application_date"],
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=11),
            ).pack(anchor="w")

            pill = status_pill(item, row["status"])
            pill.pack(side="right", padx=14)
