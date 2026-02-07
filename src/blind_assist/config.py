# Config for Blind Assist System

class Config:
    # Camera Parameters
    # Real-world dimensions (Height in meters) for Class-Specific Distance Estimation
    REAL_HEIGHTS = {
        0: 1.7,  # Person (Average height)
        2: 1.5,  # Car (Average height)
        5: 3.2,  # Bus
        7: 2.8,  # Truck
        13: 0.5, # Bench (Height of seat)
        56: 0.9  # Chair
    }
    
    # Base Focal Length (Needs calibration, but 600-800 is typical for webcams)
    FOCAL_LENGTH = 800 

    # Warning Thresholds (Meters)
    DANGER_THRESHOLD = 1.5
    WARNING_THRESHOLD = 3.0

    # Colors (B, G, R)
    COLOR_DANGER = (0, 0, 255)   # Red
    COLOR_WARNING = (0, 165, 255) # Orange
    COLOR_SAFE = (0, 255, 0)     # Green

    # Detection Settings
    CONFIDENCE_THRESHOLD = 0.5
    # COCO Class IDs: 0=person, 2=car, 5=bus, 7=truck, 13=bench, 56=chair
    TARGET_CLASSES = [0, 2, 5, 7, 13, 56]

    # System Settings
    ALERT_COOLDOWN = 3.0 # Seconds between voice alerts
