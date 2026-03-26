import tkinter as tk
from typing import Optional

import consts as const
from actions import LogicActions


class Game:
    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.title(const.GAME_TITLE)
        self.root.geometry(
            f"{const.GAME_WINDOW_SIZE_X}x{const.GAME_WINDOW_SIZE_Y}")

        self.frame = tk.Frame(self.root,
                              width=const.GAME_WINDOW_SIZE_X,
                              height=const.GAME_WINDOW_SIZE_Y)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.logic: Optional[LogicActions] = None
        self.menu: Menu = Menu(self.frame)

    def set_logic(self, logic: LogicActions) -> None:
        self.logic = logic
        self.menu.set_logic(logic)

    def show_status(self, message: str) -> None:
        self.menu.set_status(message, is_error=False)

    def run(self) -> None:
        if self.logic is None:
            raise RuntimeError(
                "Game logic is not connected. Call set_logic() before run().")
        self.root.mainloop()


class Menu:
    def __init__(self, master: tk.Widget) -> None:

        # Menu GUI setup
        self.master = master
        self.frame = tk.Frame(self.master, width=200, height=300)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0)

        self.label = tk.Label(self.frame, text="Welcome to the Menu!")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.logic: Optional[LogicActions] = None

        self.button1 = tk.Button(
            self.frame, text="Option 1", command=self._on_option_1)
        self.button1.grid(row=1, column=0, padx=10, pady=10)

        self.button2 = tk.Button(
            self.frame, text="Option 2", command=self._on_option_2)
        self.button2.grid(row=2, column=0, padx=10, pady=10)

        self.status_label = tk.Label(self.frame, text="Ready", fg="green")
        self.status_label.grid(row=3, column=0, padx=10, pady=10)

    def set_status(self, message: str, is_error: bool = False) -> None:
        self.status_label.config(
            text=message, fg="red" if is_error else "green")

    def set_logic(self, logic: LogicActions) -> None:
        self.logic = logic

    def _on_option_1(self) -> None:
        assert self.logic is not None
        self.logic.option_1()

    def _on_option_2(self) -> None:
        assert self.logic is not None
        self.logic.option_2()
