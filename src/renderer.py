from dataclasses import dataclass, field
from pathlib import Path

import tkinter as tk
from PIL import Image, ImageTk

from . import consts as const


@dataclass
class RenderState:
    x: float
    y: float
    angle_deg: float
    entity_idx: int
    texture_idx: int


class Texture:
    """Represents a texture with cached rotated versions for efficient rendering."""

    def __init__(self, name: str, base_image: Image.Image, canvas: tk.Canvas) -> None:
        self.name = name
        self.base = base_image
        self.rotated: dict[int, ImageTk.PhotoImage] = {
            0: ImageTk.PhotoImage(base_image)}
        self.canvas_id = canvas.create_image(0, 0, image=self.rotated[0])

    def get_rotated_PI(self, angle_key: int) -> ImageTk.PhotoImage:
        """Get the cached rotated texture for the given angle key, or create it if not cached."""
        texture = self.rotated.get(angle_key)
        if texture is not None:
            return texture

        rotated = self.base.rotate(
            -angle_key,
            resample=Image.Resampling.NEAREST,
            expand=True,
        )
        texture = ImageTk.PhotoImage(rotated)
        self.rotated[angle_key] = texture
        return texture


class GameRenderer:
    def __init__(self, master: tk.Widget, textures_dir: Path) -> None:
        self.render_offset_x = const.RENDER_OFFSET_X
        self.render_offset_y = const.RENDER_OFFSET_Y

        self.canvas = tk.Canvas(
            master,
            width=const.GAME_WINDOW_SIZE_X,
            height=const.GAME_WINDOW_SIZE_Y,
            highlightthickness=0,
            bg="#111111",
        )

        if Path(textures_dir).is_file():
            raise ValueError(
                f"Texture path {textures_dir} is a file, expected a directory.")
        self.texture_dir = textures_dir

        # Cache for loaded textures and their rotated versions
        self.textures: list[Texture] = []

    # Sets the canvas size based on the map size and render scaling factor
    def set_render_size(self, map_size_x: int, map_size_y: int) -> None:
        self.canvas.config(
            width=map_size_x,
            height=map_size_y,
        )
        self.render_offset_x = 0.0
        self.render_offset_y = float(map_size_y)

    def show(self) -> None:
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def hide(self) -> None:
        self.canvas.grid_remove()

    def load_textures(self, texture_files: list[str]) -> None:
        if texture_files is None or len(texture_files) == 0:
            raise ValueError("No textures specified for loading.")

        for file_name in texture_files:
            texture_path = self.texture_dir / file_name
            if not texture_path.is_file():
                raise ValueError(
                    f"Texture file {texture_path} does not exist.")

            image = Image.open(texture_path).resize(
                (const.RENDER_TEXTURE_FACTOR, const.RENDER_TEXTURE_FACTOR),
                Image.Resampling.NEAREST)
            texture = Texture(file_name, image, self.canvas)

            self.textures.append(texture)

    def resolve_texture_idx(self, texture_file: str) -> int:
        for idx, texture in enumerate(self.textures):
            if texture.name == texture_file:
                return idx
        raise ValueError(
            f"Texture file {texture_file} not found in loaded textures.")

    def render(self, states: list[RenderState]) -> None:
        # Debugging
        # Drawing boxes on the canvas to visualize the coordinate system and scaling
        self.canvas.create_rectangle(0, 0, 10, 10, fill="red")  # Origin
        self.canvas.create_rectangle(const.RENDER_POSITION_SCALE, 0,
                                     const.RENDER_POSITION_SCALE + 10, 10, fill="green")  # 1 unit on x-axis
        self.canvas.create_rectangle(0, const.RENDER_POSITION_SCALE, 10,
                                     const.RENDER_POSITION_SCALE + 10, fill="blue")  # 1 unit on y-axis

        for state in states:
            draw_angle = state.angle_deg
            if const.RENDER_INVERT_Y:
                # Y-axis inversion flips handedness, so mirror angle for display.
                draw_angle = -draw_angle

            draw_angle += const.RENDER_ANGLE_OFFSET_DEG

            angle_key = int(round(draw_angle)) % 360

            screen_x = state.x * const.RENDER_POSITION_SCALE + self.render_offset_x
            screen_y_world = -state.y if const.RENDER_INVERT_Y else state.y
            screen_y = screen_y_world * const.RENDER_POSITION_SCALE + self.render_offset_y

            state_PI = self.textures[state.texture_idx].get_rotated_PI(
                angle_key)
            self.canvas.coords(
                self.textures[state.texture_idx].canvas_id, screen_x, screen_y)
            self.canvas.itemconfig(
                self.textures[state.texture_idx].canvas_id, image=state_PI)
