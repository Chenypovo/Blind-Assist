# Config for Blind Assist System

class Config:
    # Camera Parameters
    # Real-world dimensions (Width in meters)
    REAL_WIDTHS = {
        0: 0.45,  # Person
        1: 0.4,   # Bicycle
        2: 1.8,   # Car
        3: 1.2,   # Motorcycle
        5: 2.5,   # Bus
        7: 2.5,   # Truck
        9: 2.0,   # Traffic light (usually on post)
        10: 0.8,  # Fire hydrant
        11: 0.6,  # Stop sign
        13: 1.2,  # Bench
        15: 0.5,  # Cat
        16: 0.6,  # Dog
        56: 0.5,  # Chair
        58: 0.6,  # Potted plant (Obstacle on sidewalk)
        62: 0.35, # TV/Monitor/Laptop
        63: 0.3,  # Laptop
    }
    
    # Real-world dimensions (Height in meters)
    REAL_HEIGHTS = {
        0: 1.7,   # Person
        1: 1.0,   # Bicycle
        2: 1.5,   # Car
        3: 1.2,   # Motorcycle
        5: 3.2,   # Bus
        7: 2.8,   # Truck
        9: 1.0,   # Traffic light
        10: 0.8,  # Fire hydrant
        11: 0.6,  # Stop sign
        13: 0.5,  # Bench (Seat height)
        15: 0.3,  # Cat
        16: 0.5,  # Dog
        56: 0.9,  # Chair
        58: 0.6,  # Potted plant
        62: 0.25, # Laptop/Monitor
        63: 0.25, # Laptop
    }

    # Base Focal Length (Needs calibration)
    FOCAL_LENGTH = 700 

    # Ground Plane Estimation Parameters (for Potholes)
    # Lowering horizon to 120 to give more lead time for far-away potholes
    HORIZON_Y = 120 
    CAMERA_HEIGHT = 1.2 
    MAX_GROUND_DIST = 10.0 # Cap distance at 10m to avoid 99.9m spikes

    # Warning Thresholds (Meters)
    DANGER_THRESHOLD = 1.2
    WARNING_THRESHOLD = 2.5

    # Colors (B, G, R)
    COLOR_DANGER = (0, 0, 255)   # Red
    COLOR_WARNING = (0, 165, 255) # Orange
    COLOR_SAFE = (0, 255, 0)     # Green
    
    # Detection Settings
    CONFIDENCE_THRESHOLD = 0.3
    # Comprehensive Urban Navigation Classes:
    # 0: person, 1: bicycle, 2: car, 3: motorcycle, 5: bus, 7: truck, 
    # 9: traffic light, 10: fire hydrant, 11: stop sign, 
    # 13: bench, 15: cat, 16: dog, 56: chair, 58: potted plant,
    # 62: tv, 63: laptop
    TARGET_CLASSES = [0, 1, 2, 3, 5, 7, 9, 10, 11, 13, 15, 16, 56, 58, 62, 63]
    
    # Pothole Model Settings
    POTHOLE_MODEL_PATH = "models/pothole_best.pt"
    POTHOLE_CONF_THRESHOLD = 0.4 # Potholes are harder to detect
    POTHOLE_CLASS_ID = 0 # Usually custom trained models have class 0 as the target

    # System Settings
    ALERT_COOLDOWN = 3.0 # Seconds between voice alerts
