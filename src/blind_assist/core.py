from datetime import datetime
from threading import Thread
import time
from .config import Config

class BlindAssistSystem:
    def __init__(self):
        self.last_alert_time = datetime.min
        self.history = {} # For smoothing: {object_id: [dist1, dist2, ...]}
        
    def estimate_distance(self, box_height_pixels, cls_id):
        """
        Class-Specific Monocular Distance Estimation
        Distance = (Real_Height * Focal_Length) / Image_Height
        """
        if box_height_pixels == 0:
            return 999.0
        
        # Get real height for the detected object class, default to 1.0m if unknown
        real_height = Config.REAL_HEIGHTS.get(cls_id, 1.0)
        
        distance = (real_height * Config.FOCAL_LENGTH) / box_height_pixels
        return round(distance, 2)

    def smooth_distance(self, obj_id, current_dist):
        """
        Simple Moving Average to reduce jitter.
        """
        if obj_id not in self.history:
            self.history[obj_id] = []
        
        self.history[obj_id].append(current_dist)
        if len(self.history[obj_id]) > 5: # Keep last 5 frames
            self.history[obj_id].pop(0)
            
        return round(sum(self.history[obj_id]) / len(self.history[obj_id]), 2)

    def get_warning_level(self, distance):
        """
        Determine warning level based on distance.
        """
        if distance < Config.DANGER_THRESHOLD:
            return "DANGER", Config.COLOR_DANGER
        elif distance < Config.WARNING_THRESHOLD:
            return "WARNING", Config.COLOR_WARNING
        else:
            return "SAFE", Config.COLOR_SAFE

    def should_alert(self, status):
        """
        Check if we should trigger a voice alert (with cooldown).
        """
        if status == "SAFE":
            return False

        current_time = datetime.now()
        time_diff = (current_time - self.last_alert_time).total_seconds()

        if time_diff > Config.ALERT_COOLDOWN:
            self.last_alert_time = current_time
            return True
        return False

