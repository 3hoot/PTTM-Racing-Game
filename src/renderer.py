from dataclasses import dataclass
from pathlib import Path

import tkinter as tk
from PIL import Image, ImageTk

from . import consts as const


@dataclass
class RenderState:
    x: float
    y: float
    angle_deg: float


class GameRenderer:
    def __init__(self, master: tk.Widget, textures_dir: Path) -> None:
        self.canvas = tk.Canvas(
            master,
            width=const.GAME_WINDOW_SIZE_X,
            height=const.GAME_WINDOW_SIZE_Y,
            highlightthickness=0,
            bg="#111111",
        )

        # Load base car image and create initial texture
        base_image = Image.open(textures_dir / "car_1.png").resize(
            (const.RENDER_TEXTURE_FACTOR, const.RENDER_TEXTURE_FACTOR),
            Image.Resampling.NEAREST,
        )
        self._base_car_image = base_image

        # Cache for rotated car textures
        self._car_textures: dict[int, ImageTk.PhotoImage] = {
            0: ImageTk.PhotoImage(base_image)
        }

        # Create canvas item for the player's car (for now we only have one car)

        initial_x = const.GAME_WINDOW_SIZE_X / 2
        initial_y = const.GAME_WINDOW_SIZE_Y / 2

        self._car_item_id = self.canvas.create_image(
            initial_x, initial_y, image=self._car_textures[0])

    def show(self) -> None:
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def hide(self) -> None:
        self.canvas.grid_remove()

    def render(self, state: RenderState) -> None:
        draw_angle = state.angle_deg
        if const.RENDER_INVERT_Y:
            # Y-axis inversion flips handedness, so mirror angle for display.
            draw_angle = -draw_angle
        draw_angle += const.RENDER_ANGLE_OFFSET_DEG

        angle_key = int(round(draw_angle)) % 360
        texture = self._get_or_create_texture(angle_key)

        screen_x = state.x * const.RENDER_POSITION_SCALE + const.RENDER_OFFSET_X
        screen_y_world = -state.y if const.RENDER_INVERT_Y else state.y
        screen_y = screen_y_world * const.RENDER_POSITION_SCALE + const.RENDER_OFFSET_Y

        self.canvas.coords(self._car_item_id, screen_x, screen_y)
        self.canvas.itemconfig(self._car_item_id, image=texture)

    def _get_or_create_texture(self, angle_key: int) -> ImageTk.PhotoImage:
        texture = self._car_textures.get(angle_key)
        if texture is not None:
            return texture

        rotated = self._base_car_image.rotate(
            - angle_key,
            resample=Image.Resampling.NEAREST,
            expand=True,
        )
        texture = ImageTk.PhotoImage(rotated)
        self._car_textures[angle_key] = texture
        return texture
