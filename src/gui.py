from pathlib import Path
from typing import Optional

import tkinter as tk

from . import consts as const
from .actions import LogicActions
from .input import InputController
from .menu import MenuView
from .renderer import GameRenderer, RenderState


class Game:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(const.GAME_TITLE)
        self.root.geometry(
            f"{const.GAME_WINDOW_SIZE_X}x{const.GAME_WINDOW_SIZE_Y}")
        self.root.resizable(width=False, height=False)

        # Main frame to hold either the menu(s) or the gameplay canvas
        self.frame = tk.Frame(
            self.root,
            width=const.GAME_WINDOW_SIZE_X,
            height=const.GAME_WINDOW_SIZE_Y,
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_propagate(False)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.logic: Optional[LogicActions] = None
        self._in_gameplay_view = False

        # Load textures and create renderer
        project_root = Path(__file__).resolve().parent.parent
        textures_dir = project_root / "textures"
        self.renderer = GameRenderer(self.frame, textures_dir)
        self.renderer.hide()  # Menu will be shown first

        # Create menu and input controller
        self.menu = MenuView(self.frame, on_start=self._on_start_game)
        self.input = InputController()
        self.input.bind(self.root)

    def set_logic(self, logic: LogicActions) -> None:
        self.logic = logic
        self.input.set_logic(logic)

    def run(self) -> None:
        if self.logic is None:
            raise RuntimeError(
                "Game logic is not connected. Call set_logic() before run()."
            )

        self.root.after(0, self._tick)
        self.root.mainloop()

    # Method for logic to send status messages to the menu
    # Currently unused, but can be called from logic to update the menu status label
    # (e.g. for error messages or game over)
    def status_message(self, message: str) -> None:
        self.menu.set_status(message)

    def _on_start_game(self) -> None:
        if self.logic is None or self.logic.entity_list is None:
            raise RuntimeError(
                "Game logic is not properly initialized. Ensure set_logic() is called with a valid LogicActions implementation before starting the game."
            )

        # Logic setup and start
        self.logic.is_running = True
        self.logic.set_map("map_1.json")
        self.logic.start()

        if self.logic.map is None:
            raise RuntimeError(
                "Game logic did not properly load the map. Ensure that the set_map() method of the LogicActions implementation correctly loads the map and sets the map property."
            )

        # Renderer setup
        screen_width = int(self.logic.map.size_x * const.RENDER_POSITION_SCALE)
        screen_height = int(self.logic.map.size_y *
                            const.RENDER_POSITION_SCALE)

        # Resize the main window to fit the map size
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.frame.config(width=screen_width, height=screen_height)

        # Force tkinter to process the geometry change before loading textures
        self.root.update_idletasks()

        self.renderer.load_textures({
            "car_1.png": 1.0,
            "grass_1.png": const.MAP_SCALE_FACTOR,
            "road_1.png": const.MAP_SCALE_FACTOR
        })
        self.renderer.set_render_size(
            screen_width,
            screen_height
        )

        # Assigning textures to entities (here to allow for changing textures before game start)
        self.RenderStates: list[RenderState] = []
        for idx, entity in enumerate(self.logic.entity_list):
            match entity.name:
                case "player_car":
                    texture_idx = self.renderer.resolve_texture_idx(
                        "car_1.png")
                case _ if entity.name == f"tile_{const.MAP_EMPTY_SYMBOL}":
                    texture_idx = self.renderer.resolve_texture_idx(
                        "grass_1.png")
                case _ if entity.name == f"tile_{const.MAP_ROAD_SYMBOL}":
                    texture_idx = self.renderer.resolve_texture_idx(
                        "road_1.png")
                case _:
                    raise ValueError(
                        f"Unknown entity name '{entity.name}' in logic. Ensure that the map and entity definitions use valid names that match the expected textures or add handling for new entity types in the renderer setup.")

            self.RenderStates.append(RenderState(
                0.0, 0.0, 0.0, entity_idx=idx, texture_idx=texture_idx, name=entity.name))

    def _tick(self) -> None:
        # Ensure at least 1 ms delay
        frame_ms = max(1, int(1000 / const.GAME_TARGET_FPS))

        dt = frame_ms / 1000.0  # Convert ms to seconds for logic update

        if self.logic is not None and self.logic.is_running:
            if not self._in_gameplay_view:
                self.menu.hide()
                self.renderer.show()
                self._in_gameplay_view = True
                self.input.set_enabled(True)
                self.root.focus_set()

            self.logic.update(dt)
            self._render_from_logic()
        else:
            if self._in_gameplay_view:
                self.renderer.hide()
                self.menu.show()
                self._in_gameplay_view = False
                self.input.set_enabled(False)

        self.root.after(frame_ms, self._tick)

    def _render_from_logic(self) -> None:
        if self.logic is None or self.logic.entity_list is None:
            raise RuntimeError(
                "Game logic is not properly initialized. Ensure set_logic() is called with a valid LogicActions implementation before starting the game."
            )

        # Update all positions and angles from logic entities
        for state in self.RenderStates:
            logic_entity = self.logic.entity_list[state.entity_idx]
            state.x = logic_entity.position.x
            state.y = logic_entity.position.y
            state.angle_deg = logic_entity.rotation

        self.renderer.render(self.RenderStates)
