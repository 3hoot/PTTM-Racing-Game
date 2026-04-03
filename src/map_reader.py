from enum import Enum
from dataclasses import dataclass, field
import numpy as np
import json

from .coords import Coords
from . import consts as const


class MapFileType(Enum):
    JSON = 0


@dataclass
class MapData:
    symbolic_map_matrix: np.matrix
    traction_map_matrix: np.matrix
    start_position: Coords = field(default_factory=lambda: Coords(0.0, 0.0))
    end_position: Coords = field(default_factory=lambda: Coords(0.0, 0.0))
    size_x: int = 0
    size_y: int = 0


class MapReader():
    def read_map(self, file_path: str,
                 file_type: MapFileType) -> MapData:

        match file_type:
            case MapFileType.JSON:
                return self._read_json_map(file_path)
            case _:
                raise ValueError(f"Unsupported map file type: {file_type}")

    def _read_json_map(self, file_path: str) -> MapData:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

                # Store symbolic map as-is
                symbolic_map_matrix = np.matrix(data["map"], dtype=object)

                # Create traction map by replacing symbols with friction coefficients
                tile_friction = data["tile_friction"]
                traction_grid = [
                    [tile_friction[symbol] for symbol in row]
                    for row in data["map"]
                ]
                traction_map_matrix = np.matrix(traction_grid, dtype=float)

                # Extract start and end positions
                start_position = Coords(
                    data["start_position"][0], data["start_position"][1])
                end_position = Coords(
                    data["end_position"][0], data["end_position"][1])

                return MapData(
                    symbolic_map_matrix=symbolic_map_matrix,
                    traction_map_matrix=traction_map_matrix,
                    start_position=start_position,
                    end_position=end_position,
                    size_x=int(len(data["map"][0]) * const.MAP_SCALE_FACTOR),
                    size_y=int(len(data["map"]) * const.MAP_SCALE_FACTOR)
                )

        except FileNotFoundError:
            print(f"Error: Map file '{file_path}' not found.")
            raise
        except KeyError as e:
            print(f"Error: Missing key in map file: {e}")
            raise
        except json.JSONDecodeError:
            print(f"Error: Map file '{file_path}' is not valid JSON.")
            raise
        except Exception as e:
            print(
                f"Error: Unexpected error reading map file '{file_path}': {e}")
            raise
