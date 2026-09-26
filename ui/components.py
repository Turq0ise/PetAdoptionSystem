from pathlib import Path
import customtkinter as ctk
from PIL import Image

from ui.theme import COLORS, STATUS_COLORS


def clear_children(widget):
    for child in widget.winfo_children():
        child.destroy()


def page_title(parent, eyebrow, title, subtitle):
    wrap = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(
        wrap,
        text=eyebrow.upper(),
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color=COLORS["primary_dark"],
    ).pack(anchor="w")

    ctk.CTkLabel(
        wrap,
        text=title,
        font=ctk.CTkFont(size=30, weight="bold"),
        text_color=COLORS["text"],
    ).pack(anchor="w", pady=(3, 1))

    ctk.CTkLabel(
        wrap,
        text=subtitle,
        font=ctk.CTkFont(size=13),
        text_color=COLORS["muted"],
    ).pack(anchor="w")
    return wrap


def make_card(parent, **kwargs):
    options = {
        "fg_color": COLORS["card"],
        "corner_radius": 20,
        "border_width": 1,
        "border_color": COLORS["line"],
    }
    options.update(kwargs)
    return ctk.CTkFrame(parent, **options)


def status_pill(parent, status):
    bg, fg = STATUS_COLORS.get(
        status,
        (COLORS["secondary_soft"], COLORS["text"])
    )
    return ctk.CTkLabel(
        parent,
        text=f"  {status}  ",
        fg_color=bg,
        text_color=fg,
        corner_radius=999,
        font=ctk.CTkFont(size=11, weight="bold"),
        height=26,
    )


def load_pet_image(path, size=(160, 120)):
    if not path:
        return None

    file_path = Path(path)
    if not file_path.exists():
        return None

    try:
        image = Image.open(file_path)
        return ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=size,
        )
    except Exception:
        return None


def cute_button(parent, text, command=None, secondary=False, danger=False, width=120):
    if danger:
        fg = COLORS["danger_soft"]
        hover = "#F7D1D1"
        text_color = "#A74E4E"
    elif secondary:
        fg = COLORS["secondary_soft"]
        hover = "#E3D8F8"
        text_color = "#6B56A3"
    else:
        fg = COLORS["primary"]
        hover = COLORS["primary_dark"]
        text_color = "#FFFFFF"

    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=38,
        corner_radius=14,
        fg_color=fg,
        hover_color=hover,
        text_color=text_color,
        font=ctk.CTkFont(size=13, weight="bold"),
    )
