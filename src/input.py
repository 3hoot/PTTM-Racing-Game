import tkinter as tk
from typing import Optional

from .actions import LogicActions
from . import consts as const


class InputController:
    def __init__(self) -> None:
        self._logic: Optional[LogicActions] = None
        self._enabled = False

    def set_logic(self, logic: LogicActions) -> None:
        self._logic = logic

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def bind(self, widget: tk.Misc) -> None:
        widget.bind("<KeyPress-Up>", self._on_up_press)
        widget.bind("<KeyRelease-Up>", self._on_up_release)
        widget.bind("<KeyPress-Down>", self._on_down_press)
        widget.bind("<KeyRelease-Down>", self._on_down_release)
        widget.bind("<KeyPress-Left>", self._on_left_press)
        widget.bind("<KeyRelease-Left>", self._on_left_release)
        widget.bind("<KeyPress-Right>", self._on_right_press)
        widget.bind("<KeyRelease-Right>", self._on_right_release)

    def _can_process_input(self) -> bool:
        return self._enabled and self._logic is not None and self._logic.is_running

    def _on_up_press(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("accelerate", 1.0)

    def _on_up_release(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("accelerate", 0.0)

    def _on_down_press(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("brake", 1.0)

    def _on_down_release(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("brake", 0.0)

    def _on_left_press(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("steer", 1.0)

    def _on_left_release(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("steer", 0.0)

    def _on_right_press(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("steer", -1.0)

    def _on_right_release(self, _event: tk.Event) -> None:
        if self._can_process_input():
            assert self._logic is not None
            self._logic.input("steer", 0.0)
