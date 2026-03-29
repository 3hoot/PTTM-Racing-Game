from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .map_reader import MapData
    from .logic import CarEntity


class LogicActions(Protocol):
    def start(self) -> None: ...
    def update(self, dt: float) -> None: ...
    def input(self, action: str, value: float) -> None: ...
    is_running: bool
    map: "MapData | None"
    player: "CarEntity | None"


class GuiActions(Protocol):
    def status_message(self, message: str) -> None: ...
