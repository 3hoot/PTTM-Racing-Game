
# --- GUI related constants ---
GAME_TITLE: str = "Pedal To The Metal - Racing Game"
GAME_WINDOW_SIZE_X: int = 1600
GAME_WINDOW_SIZE_Y: int = 1800
GAME_FPS: int = 30

# Render transform controls (screen-space only)
RENDER_POSITION_SCALE: float = 30.0
RENDER_TEXTURE_FACTOR: int = 100
RENDER_OFFSET_X: float = 0.0
RENDER_OFFSET_Y: float = float(GAME_WINDOW_SIZE_Y)
RENDER_INVERT_Y: bool = True
# Use this to align sprite forward direction with logic zero-angle direction.
RENDER_ANGLE_OFFSET_DEG: float = 0.0

# --- Car physics related constants ---
DEFAULT_MASS: float = 800.0                # [kg]
DEFAULT_WHEELBASE: float = 2.5             # [m]
DEFAULT_MASS_DISTRIBUTION: float = 0.5     # 0.3 equals 30% front, 70% rear
DEFAULT_MASS_HEIGHT: float = 0.5           # [m], height of the center of mass
DEFAULT_INERTIA: float = 1200.0            # [kg*m^2]
DEFAULT_TIRE_FRICTION_COEFF: float = 0.9   # mu, value is for dry asphalt
DEFAULT_CORNERING_STIFFNESS: float = 80.0  # Force per degree of slip
DEFAULT_ACCEL_FORCE: float = 1000.0        # Engine power
DEFAULT_BRAKE_FORCE: float = 2200.0        # Braking power
# [degrees], maximum steer angle at full input
DEFAULT_MAX_STEER_ANGLE: float = 50.0

# --- World physics related constants ---
WORLD_GRAVITY: float = 9.81
DEFAULT_AIR_RESISTANCE_COEFF: float = 0.3  # Aerodynamic drag coefficient
DEFAULT_ROLLING_RESISTANCE_COEFF: float = 0.01  # Rolling resistance coefficient

# --- Calculation related constants ---
# [m/s], below this we consider the car stopped
MIN_VELOCITY_THRESHOLD: float = 0.01

# --- Map format related constants (mainly for gui) ---
MAP_ROAD_SYMBOL: str = "X"
MAP_EMPTY_SYMBOL: str = "_"
MAP_SCALE_FACTOR: float = 16
