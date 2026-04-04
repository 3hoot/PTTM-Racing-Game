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
    entity_idx: int
    texture_idx: int
    name: str
    canvas_id: int | None = None


class Texture:
    """Represents a texture with cached rotated versions for efficient rendering."""

    def __init__(self, name: str, base_image: Image.Image) -> None:
        self.name = name
        self.base = base_image
        self.rotated: dict[int, ImageTk.PhotoImage] = {
            0: ImageTk.PhotoImage(base_image)}

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
        self.render_offset_y = float(
            map_size_y) if const.RENDER_INVERT_Y else 0.0

    def show(self) -> None:
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def hide(self) -> None:
        self.canvas.grid_remove()

    # Load textures based on the provided mapping of texture file names to scaling factors
    def load_textures(self, texture_files: dict[str, float]) -> None:
        if texture_files is None or len(texture_files) == 0:
            raise ValueError("No textures specified for loading.")

        for file_name, scale_factor in texture_files.items():

            # Check if the texture is already loaded to avoid duplicates
            if any(tex.name == file_name for tex in self.textures):
                continue

            # Load texture image and create Texture object
            texture_path = self.texture_dir / file_name
            if not texture_path.is_file():
                raise ValueError(
                    f"Texture file {texture_path} does not exist.")

            image = Image.open(texture_path).resize(
                (int(const.RENDER_TEXTURE_FACTOR * scale_factor),
                 int(const.RENDER_TEXTURE_FACTOR * scale_factor)),
                Image.Resampling.NEAREST)

            texture = Texture(file_name, image)

            self.textures.append(texture)

    # Helper methods
    # resolve texture and entity indices based on names
    # for easier mapping from logic to renderer
    def resolve_texture_idx(self, texture_file: str) -> int:
        for idx, texture in enumerate(self.textures):
            if texture.name == texture_file:
                return idx
        raise ValueError(
            f"Texture file {texture_file} not found in loaded textures.")

    def resolve_entity_idx(self, entity_name: str, entity_list: list) -> int:
        for idx, entity in enumerate(entity_list):
            if hasattr(entity, "name") and entity.name == entity_name:
                return idx
        raise ValueError(
            f"Entity with name {entity_name} not found in entity list.")

    def render(self, states: list[RenderState]) -> None:

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

            # If the canvas item doesn't exist yet, create it.
            # Otherwise, just update its position and image.
            if state.canvas_id is None:
                state.canvas_id = self.canvas.create_image(
                    screen_x,
                    screen_y,
                    image=state_PI,
                )
            else:
                self.canvas.coords(state.canvas_id, screen_x, screen_y)
                self.canvas.itemconfig(state.canvas_id, image=state_PI)

            # Special state handling
            match state.name:
                case "player_car":
                    # Raise player car above other entities
                    # to ensure it's visible on top of the map tiles.
                    if state.canvas_id is not None:
                        self.canvas.tag_raise(state.canvas_id)
