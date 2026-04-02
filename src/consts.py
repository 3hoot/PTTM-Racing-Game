
# --- GUI related constants ---
GAME_TITLE: str = "Pedal To The Metal - Racing Game"
GAME_GLOBAL_SCALE: float = 0.8
GAME_WINDOW_SIZE_X: int = int(1600 * GAME_GLOBAL_SCALE)
GAME_WINDOW_SIZE_Y: int = int(1800 * GAME_GLOBAL_SCALE)
GAME_TARGET_FPS: int = 60

# Render transform controls (screen-space only)
RENDER_POSITION_SCALE: float = 60.0 * GAME_GLOBAL_SCALE
RENDER_TEXTURE_FACTOR: int = int(60 * GAME_GLOBAL_SCALE)
RENDER_OFFSET_X: float = 0.0
RENDER_OFFSET_Y: float = float(GAME_WINDOW_SIZE_Y)
# Account for y-axis inversion between world and screen coordinates``
RENDER_INVERT_Y: bool = True
# Use this to align sprite forward direction with logic zero-angle direction.
RENDER_ANGLE_OFFSET_DEG: float = 0.0

# --- Car physics related constants ---
DEFAULT_MASS: float = 1500.0                # [kg]
DEFAULT_WHEELBASE: float = 3             # [m]
DEFAULT_MASS_DISTRIBUTION: float = 0.5     # 0.3 equals 30% front, 70% rear
DEFAULT_MASS_HEIGHT: float = 0.5           # [m], height of the center of mass
DEFAULT_INERTIA: float = 1200.0            # [kg*m^2]
DEFAULT_TIRE_FRICTION_COEFF: float = 0.9   # mu, value is for dry asphalt
DEFAULT_CORNERING_STIFFNESS: float = 100.0  # Force per degree of slip
DEFAULT_ACCEL_FORCE: float = 3500.0        # Engine power
DEFAULT_BRAKE_FORCE: float = 6000.0        # Braking power
# [degrees], maximum steer angle at full input
DEFAULT_MAX_STEER_ANGLE: float = 55.0
# Higher values make the car understeer more as speed rises.
DEFAULT_UNDERSTEER_GAIN: float = 0.015

# --- World physics related constants ---
WORLD_GRAVITY: float = 9.81
DEFAULT_AIR_RESISTANCE_COEFF: float = 0.6  # Aerodynamic drag coefficient
DEFAULT_ROLLING_RESISTANCE_COEFF: float = 0.04  # Rolling resistance coefficient

# --- Calculation related constants ---
# [m/s], below this we consider the car stopped
MIN_VELOCITY_THRESHOLD: float = 0.01

# --- Map format related constants (mainly for gui) ---
MAP_ROAD_SYMBOL: str = "X"
MAP_EMPTY_SYMBOL: str = "_"
MAP_SCALE_FACTOR: float = 16
