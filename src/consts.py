
# --- GUI related constants ---
GAME_TITLE: str = "Pedal To The Metal - Racing Game"
GAME_WINDOW_SIZE_X: int = 1200
GAME_WINDOW_SIZE_Y: int = 800
GAME_FPS: int = 30
GAME_SCALE_FACTOR: int = 100

# Render transform controls (screen-space only)
RENDER_POSITION_SCALE: float = 20.0
RENDER_OFFSET_X: float = 30.0
RENDER_OFFSET_Y: float = 30.0

# --- Car physics related constants ---
DEFAULT_MASS: float = 800.0                # [kg]
DEFAULT_WHEELBASE: float = 2.5             # [m]
DEFAULT_MASS_DISTRIBUTION: float = 0.5     # 0.3 equals 30% front, 70% rear
DEFAULT_MASS_HEIGHT: float = 0.5           # [m], height of the center of mass
DEFAULT_INERTIA: float = 1200.0            # [kg*m^2]
DEFAULT_TIRE_FRICTION_COEFF: float = 0.9   # mu, value is for dry asphalt
DEFAULT_CORNERING_STIFFNESS: float = 20.0  # Force per degree of slip
DEFAULT_ACCEL_FORCE: float = 500.0        # Engine power
DEFAULT_BRAKE_FORCE: float = 800.0        # Braking power
# How quickly the steering returns to center
DEFAULT_STEER_CENTERING_COEFF: float = 0.0
# Multiplier for how much the steer input affects the steer angle
DEFAULT_STEER_MULTIPLIER: float = 3.0
# [degrees], maximum steer angle at full input
DEFAULT_MAX_STEER_ANGLE: float = 50.0

# --- World physics related constants ---
WORLD_GRAVITY: float = 9.81
DEFAULT_AIR_RESISTANCE_COEFF: float = 0.6  # Aerodynamic drag coefficient
DEFAULT_ROLLING_RESISTANCE_COEFF: float = 0.02  # Rolling resistance coefficient

# --- Calculation related constants ---
# [m/s], below this we consider the car stopped
MIN_VELOCITY_THRESHOLD: float = 0.01

# --- Map format related constants (mainly for gui) ---
MAP_ROAD_SYMBOL: str = "X"
MAP_EMPTY_SYMBOL: str = "_"
MAP_SCALE_FACTOR: float = 16
