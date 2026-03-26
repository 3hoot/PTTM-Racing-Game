from typing import Protocol


class LogicActions(Protocol):
    def option_1(self) -> None: ...
    def option_2(self) -> None: ...


class GuiActions(Protocol):
    def show_status(self, message: str) -> None: ...
