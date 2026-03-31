from pathlib import Path
from typing import Optional

import tkinter as tk

from . import consts as const
from .actions import LogicActions
from .input import InputController
from .menu import MenuView, SecondWindow
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

        # Create menu and input controller
        self.menu = MenuView(self.frame, on_start=self._on_start_game)
        self.input = InputController()
        self.input.bind(self.root)

        # Load textures and create renderer
        project_root = Path(__file__).resolve().parent.parent
        textures_dir = project_root / "textures"
        texture_file = self.menu.selected_texture
        print("GUI texture_file =", texture_file)
        self.renderer = GameRenderer(self.frame, textures_dir, texture_file)
        self.renderer.hide()  # Menu will be shown first


    def second_window(self) -> None:
        self.new_win = tk.Toplevel(self.root)
        self.new_win.geometry('300x300')
        self.second_menu = SecondWindow(self.new_win)
        
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
    def status_message(self, message: str) -> None:
        self.menu.set_status(message)

    def _on_start_game(self) -> None:
        self.renderer.selected_texture = self.menu.selected_texture
        self.renderer.draw_background()
        self.menu.hide()
        self.renderer.show()
        
        if self.logic is None:
            return
        self.logic.start()

    def _tick(self) -> None:
        # Ensure at least 1 ms delay
        frame_ms = max(1, int(1000 / const.GAME_FPS))

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
        if self.logic is None or self.logic.player is None:
            return

        player = self.logic.player
        state = RenderState(
            x=player.position.x,
            y=player.position.y,
            angle_deg=player.rotation,
        )
        self.renderer.render(state)
