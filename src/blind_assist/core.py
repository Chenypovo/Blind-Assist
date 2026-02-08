from datetime import datetime
from threading import Thread
import time
from .config import Config

class BlindAssistSystem:
    def __init__(self):
        self.last_alert_time = datetime.min
        self.history = {} # For smoothing: {object_id: [dist1, dist2, ...]}
        
    def estimate_distance_ground(self, box_bottom_y):
        """
        Distance Estimation for Ground Objects (Potholes)
        """
        if box_bottom_y <= Config.HORIZON_Y:
            return Config.MAX_GROUND_DIST
            
        pixel_diff = box_bottom_y - Config.HORIZON_Y
        k = 300.0 
        
        distance = k / pixel_diff
        # Clamp to reasonable range
        if distance > Config.MAX_GROUND_DIST:
            distance = Config.MAX_GROUND_DIST
            
        return round(distance, 2)

    def estimate_distance(self, box_w_pixels, box_h_pixels, cls_id):
        """
        Improved Distance Estimation using both Width and Height.
        Distance = (Real_Dimension * Focal_Length) / Pixel_Dimension
        """
        if box_w_pixels == 0 or box_h_pixels == 0:
            return 999.0
        
        # 1. Try Width-based estimation (usually more robust to posture/occlusion)
        real_width = Config.REAL_WIDTHS.get(cls_id)
        dist_w = (real_width * Config.FOCAL_LENGTH) / box_w_pixels if real_width else None
        
        # 2. Try Height-based estimation
        real_height = Config.REAL_HEIGHTS.get(cls_id)
        dist_h = (real_height * Config.FOCAL_LENGTH) / box_h_pixels if real_height else None
        
        # 3. Fuse the results
        if dist_w and dist_h:
            # Simple average of both estimations
            distance = (dist_w + dist_h) / 2
        elif dist_w:
            distance = dist_w
        elif dist_h:
            distance = dist_h
        else:
            # Fallback for unknown classes
            distance = (0.5 * Config.FOCAL_LENGTH) / ((box_w_pixels + box_h_pixels) / 2)
            
        return round(distance, 2)

    def smooth_distance(self, obj_id, current_dist):
        """
        Simple Moving Average to reduce jitter.
        """
        if current_dist >= 99.0: # Skip outliers/infinite detections
            return current_dist

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

    def get_direction(self, box_center_x, frame_width):
        """
        Calculate precise direction based on horizontal position (O'clock format).
        12 o'clock is straight ahead.
        """
        # Normalize center_x to -1 (left) to 1 (right)
        relative_pos = (box_center_x / frame_width) * 2 - 1
        
        # Map -1 to 1 to a 10 to 2 o'clock range (roughly 120 degree FOV)
        # -1.0 -> 10 o'clock
        # -0.5 -> 11 o'clock
        #  0.0 -> 12 o'clock
        #  0.5 -> 1 o'clock
        #  1.0 -> 2 o'clock
        
        if relative_pos < -0.7:
            return "at 10 o'clock"
        elif relative_pos < -0.2:
            return "at 11 o'clock"
        elif relative_pos < 0.2:
            return "straight ahead"
        elif relative_pos < 0.7:
            return "at 1 o'clock"
        else:
            return "at 2 o'clock"

    def trigger_audio_alert(self, message):
        """
        Proactive alarm using Mac 'say' command in a background thread.
        """
        def speak():
            import os
            # Ensure the message is treated as a single string for shell
            # Using -v Samantha for a more natural voice (if available)
            safe_message = message.replace("'", "")
            os.system(f"say -v Samantha '{safe_message}' || say '{safe_message}'")
            
        alert_thread = Thread(target=speak)
        alert_thread.daemon = True
        alert_thread.start()

