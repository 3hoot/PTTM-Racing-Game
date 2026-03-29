import tkinter as tk
from typing import Callable

from . import consts as const


class MenuView:
    def __init__(self, master: tk.Widget, on_start: Callable[[], None]) -> None:
        self.frame = tk.Frame(master, width=300, height=220)
        self.frame.grid(row=0, column=0)

        self.title_label = tk.Label(
            self.frame,
            text=const.GAME_TITLE,
            font=("Arial", 16),
        )
        self.title_label.grid(row=0, column=0, padx=12, pady=(16, 10))

        self.start_button = tk.Button(
            self.frame,
            text="Start Game",
            command=on_start,
            width=16,
        )
        self.start_button.grid(row=1, column=0, padx=12, pady=(8, 8))

        self.status_label = tk.Label(self.frame, text="", wraplength=260)
        self.status_label.grid(row=2, column=0, padx=12, pady=(8, 12))

    def show(self) -> None:
        self.frame.grid()

    def hide(self) -> None:
        self.frame.grid_remove()

    def set_status(self, message: str) -> None:
        self.status_label.configure(text=message)
