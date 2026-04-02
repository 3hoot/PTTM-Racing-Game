from typing import Optional
from enum import Enum
import numpy as np
from pathlib import Path
import copy

from . import consts as const
from . import map_reader as mp
from .actions import GuiActions
from .coords import Coords


class Game:
    def __init__(self, ui: Optional[GuiActions]) -> None:
        self.ui: Optional[GuiActions] = ui
        self.is_running: bool = False
        self.map: Optional[mp.MapData] = None
        self.player: Optional["CarEntity"] = None
        self.entity_list: list["Entity"] = []

    def set_ui(self, ui: GuiActions) -> None:
        self.ui = ui

    # --- Game logic ---

    def start(self, map_num: int = 1) -> None:
        if self.ui is None:
            raise RuntimeError(
                "UI is not connected. Call set_ui() before start().")

        # Initialize game state, create car entity, etc.
        self.is_running: bool = True
        maps_dir = Path(__file__).resolve().parent.parent / "maps"
        self.map = mp.MapReader().read_map(
            str(maps_dir / f"map_{map_num}.json"), mp.MapFileType.JSON)

        # Start at the center of the starting tile
        scaled_start_position = Coords(self.map.start_position.x * const.MAP_SCALE_FACTOR +
                                       0.5 * const.MAP_SCALE_FACTOR,
                                       self.map.start_position.y * const.MAP_SCALE_FACTOR +
                                       0.5 * const.MAP_SCALE_FACTOR)

        # for now we'll just start at the world origin until we implement map boundaries and collision
        scaled_start_position = Coords(0.0, 0.0)

        self.player = CarEntity(position=scaled_start_position)

        # For future expansion to handle multiple entities (cars and tiles)
        self.entity_list: list[Entity] = [self.player]

    def input(self, action: str, value: float) -> None:
        if not self.is_running:
            return

        if self.player is None:
            return

        if action == "accelerate":
            self.player.setAccelerate(value)
        elif action == "brake":
            self.player.setBrake(value)
        elif action == "steer":
            self.player.setSteer(value)

    def update(self, dt: float) -> None:
        if not self.is_running:
            return

        # if self.player is None or self.map is None:
        #     return

        if self.player is None:
            return

        # Update game state, physics, etc.
        self.player.update(dt)

        # Debug print for player's position and rotation
        print(
            f"Player position: ({self.player.position.x:.2f}, {self.player.position.y:.2f}), rotation: {self.player.rotation:.2f} degrees")
        print(
            f"Player accelerate: {self.player.throttle:.2f}, brake: {self.player.brake:.2f}, steer angle: {self.player.steer_angle:.2f}")

        # for entity in self.entity_list:
        #     # Determine which tile the car is on and update tire friction accordingly
        #     tile_x = int(entity.position.x // const.MAP_SCALE_FACTOR)
        #     tile_y = int(entity.position.y // const.MAP_SCALE_FACTOR)

        #     # Check for out-of-bounds (off the map) before map indexing
        #     if tile_x < 0 or tile_x >= self.map.symbolic_map_matrix.shape[1] or tile_y < 0 or tile_y >= self.map.symbolic_map_matrix.shape[0]:
        #         self.is_running = False
        #         # self.ui.status_message(
        #         #     "Game Over! You've gone off the track and fell into a ditch!")
        #         continue

        #     entity.tire_friction_coeff = self.map.traction_map_matrix[tile_y, tile_x]

        #     # Check for win condition (reaching end tile)
        #     if (tile_x, tile_y) == (int(self.map.end_position.x), int(self.map.end_position.y)):
        #         self.is_running = False
        #         # self.ui.status_message(
        #         #     "Congratulations! You've reached the finish line!")


class CarType(Enum):
    RWD = 0
    FWD = 1
    AWD = 2


class Entity:
    def __init__(self, position: Optional[Coords], rotation: float) -> None:
        self.position = position if position is not None else Coords(0.0, 0.0)
        self.rotation = rotation


class CarEntity(Entity):
    def __init__(self, position=Coords(10.0, 10.0),
                 rotation=0.0,
                 wheelbase=const.DEFAULT_WHEELBASE,
                 mass_distribution=const.DEFAULT_MASS_DISTRIBUTION,
                 mass_height=const.DEFAULT_MASS_HEIGHT,
                 mass=const.DEFAULT_MASS,
                 inertia=const.DEFAULT_INERTIA,
                 tire_friction_coeff=const.DEFAULT_TIRE_FRICTION_COEFF,
                 cornering_stiffness=const.DEFAULT_CORNERING_STIFFNESS,
                 car_type=CarType.AWD) -> None:

        super().__init__(position, rotation)

        # Car state
        self.wheelbase = wheelbase
        self.mass_distribution = mass_distribution
        self.mass_height = mass_height
        self.mass = mass
        self.inertia = inertia
        self.car_type = car_type

        # Local velocity: x is lateral, y is longitudinal
        self.velocity = Coords(0.0, 0.0)
        self.prev_velocity = Coords(0.0, 0.0)
        self.angular_velocity = 0.0
        self.steer_angle = 0.0  # Degrees
        self.brake = 0.0  # 0 to 1
        self.throttle = 0.0  # 0 to 1
        self.speed = 0.0  # Scalar speed for convenience

        # Physics Constants
        self.cornering_stiffness = cornering_stiffness
        self.tire_friction_coeff = tire_friction_coeff

    def update(self, dt: float) -> None:

        # --- Calculate weight on front/rear axles ---
        long_accel = (self.velocity.y - self.prev_velocity.y) / \
            dt if dt > const.MIN_VELOCITY_THRESHOLD else 0.0

        # Store previous velocity for next update
        self.prev_velocity = copy.copy(self.velocity)

        front_weight_transfer = long_accel * self.mass * self.mass_height / self.wheelbase
        weight_front = self.mass * const.WORLD_GRAVITY * \
            self.mass_distribution - front_weight_transfer
        weight_rear = self.mass * const.WORLD_GRAVITY * \
            (1 - self.mass_distribution) + front_weight_transfer

        # Clamping weights to avoid negative values (can happen under extreme braking)
        weight_front = max(weight_front, 0.0)
        weight_rear = max(weight_rear, 0.0)

        # Input forces
        accel_force = self.throttle * const.DEFAULT_ACCEL_FORCE
        brake_force = self.brake * \
            const.DEFAULT_BRAKE_FORCE if self.velocity.y > 0.0 else 0.0

        # Self explanatory
        # Used for biasing acceleration
        match self.car_type:
            case CarType.RWD:
                front_accel_force_long_coeff = 0.0
                rear_accel_force_long_coeff = 1.0
            case CarType.FWD:
                front_accel_force_long_coeff = 1.0
                rear_accel_force_long_coeff = 0.0
            case CarType.AWD:
                front_accel_force_long_coeff = 0.5
                rear_accel_force_long_coeff = 0.5

        # --- Lateral forces calculations ---
        # Calculate Slip Angles
        # Front slip = atan(lat_vel + angular_vel * dist_to_front / long_vel) - steer_angle
        if abs(self.velocity.y) > const.MIN_VELOCITY_THRESHOLD:  # Avoid division by zero
            slip_angle_front = np.degrees(np.arctan2(
                self.velocity.x + self.angular_velocity * self.wheelbase *
                (1-self.mass_distribution), abs(self.velocity.y))) - self.steer_angle
            slip_angle_rear = np.degrees(np.arctan2(
                self.velocity.x - self.angular_velocity * self.wheelbase *
                self.mass_distribution, abs(self.velocity.y)))
        else:
            slip_angle_front = slip_angle_rear = 0.0

        # Calculate Lateral Forces
        # F = -stiffness * slip_angle
        force_front_lat = -self.cornering_stiffness * slip_angle_front
        force_rear_lat = -self.cornering_stiffness * slip_angle_rear

        # --- Longitudinal forces ---
        force_front_long = accel_force * front_accel_force_long_coeff - brake_force
        force_rear_long = accel_force * rear_accel_force_long_coeff - brake_force

        # --- Friction circle calculations ---
        # Combined tire forces per axle must stay within the friction circle.
        friction_force_front = self.tire_friction_coeff * weight_front
        friction_force_rear = self.tire_friction_coeff * weight_rear

        input_forces_front = np.hypot(force_front_long, force_front_lat)
        if input_forces_front > friction_force_front and input_forces_front > 0.0:
            scale = friction_force_front / input_forces_front
            force_front_long *= scale
            force_front_lat *= scale

        input_forces_rear = np.hypot(force_rear_long, force_rear_lat)
        if input_forces_rear > friction_force_rear and input_forces_rear > 0.0:
            scale = friction_force_rear / input_forces_rear
            force_rear_long *= scale
            force_rear_lat *= scale

        # --- Calculate Total Forces and Resultant Acceleration ---
        drag_force_lat = - const.DEFAULT_AIR_RESISTANCE_COEFF * self.velocity.x * \
            abs(self.velocity.x) - const.DEFAULT_ROLLING_RESISTANCE_COEFF * \
            self.velocity.x * self.mass
        total_force_lat = force_front_lat + force_rear_lat + drag_force_lat

        drag_force_long = - const.DEFAULT_AIR_RESISTANCE_COEFF * self.velocity.y * \
            abs(self.velocity.y) - const.DEFAULT_ROLLING_RESISTANCE_COEFF * \
            self.velocity.y * self.mass
        total_force_long = force_front_long + force_rear_long + drag_force_long

        # --- Integrate Physics ---
        # Acceleration = Force / Mass
        accel_lat = total_force_lat / self.mass
        self.velocity.x += accel_lat * dt

        accel_long = total_force_long / self.mass
        self.velocity.y += accel_long * dt

        # Simple anti-overshoot rule: braking while moving forward should
        # stop at zero, not instantly create reverse speed.
        if self.brake > 0.0 and self.prev_velocity.y > 0.0 and self.velocity.y < 0.0:
            self.velocity.y = 0.0

        # Calculate angular velocity based on longitudinal velocity and steering angle
        self.speed = np.hypot(self.velocity.x, self.velocity.y)
        if self.speed > const.MIN_VELOCITY_THRESHOLD:
            speed_factor = 1.0 / \
                (1.0 + const.DEFAULT_UNDERSTEER_GAIN * (self.speed**2))
            self.angular_velocity = (
                self.velocity.y / self.wheelbase
            ) * np.tan(np.radians(self.steer_angle)) * speed_factor
        else:
            self.angular_velocity = 0.0

        self.rotation += np.degrees(self.angular_velocity) * dt
        self.rotation = self.rotation % 360  # Keep rotation within [0, 360)

        self.velocity.x *= max(0.0, 1.0 - 4.0 * dt)

        # --- Convert Local Velocity to World Position ---
        rad = np.radians(self.rotation)
        world_vx = np.cos(rad) * self.velocity.x - \
            np.sin(rad) * self.velocity.y
        world_vy = np.sin(rad) * self.velocity.x + \
            np.cos(rad) * self.velocity.y

        self.position.x += world_vx * dt
        self.position.y += world_vy * dt

    def setAccelerate(self, amount: float) -> None:
        self.throttle = np.clip(amount, 0.0, 1.0)

    def setBrake(self, amount: float) -> None:
        self.brake = np.clip(amount, 0.0, 1.0)

    def setSteer(self, steer_input: float) -> None:
        # steer_input is expected in [-1, 1]. Map it directly to wheel angle.
        steer_input = np.clip(steer_input, -1.0, 1.0)
        self.steer_angle = steer_input * const.DEFAULT_MAX_STEER_ANGLE
