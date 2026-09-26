COLORS = {
    "background": "#FFF8FB",
    "sidebar": "#FFF0F6",
    "card": "#FFFFFF",
    "primary": "#E887B1",
    "primary_dark": "#A94F78",
    "primary_soft": "#FAD9E8",
    "secondary": "#BCA7E8",
    "secondary_soft": "#EEE7FA",
    "mint": "#BDE6D5",
    "mint_dark": "#4E8C73",
    "yellow": "#F7DFA3",
    "yellow_dark": "#9A7422",
    "danger": "#E47A7A",
    "danger_soft": "#FBE3E3",
    "text": "#493E45",
    "muted": "#8B7D86",
    "line": "#F0DCE7",
    "hover": "#FCE2EE",
}

STATUS_COLORS = {
    "Available": (COLORS["mint"], COLORS["mint_dark"]),
    "Pending": (COLORS["yellow"], COLORS["yellow_dark"]),
    "Adopted": (COLORS["secondary_soft"], "#6B56A3"),
    "Approved": (COLORS["mint"], COLORS["mint_dark"]),
    "Rejected": (COLORS["danger_soft"], "#A74E4E"),
}
