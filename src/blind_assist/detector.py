import cv2
from ultralytics import YOLO
from .config import Config
from .core import BlindAssistSystem

class Detector:
    def __init__(self, model_path='yolov8n.pt'):
        # Model 1: General Obstacles (People, Cars)
        self.model_general = YOLO(model_path)
        
        # Model 2: Pothole Specialist (Your trained model)
        self.model_pothole = YOLO(Config.POTHOLE_MODEL_PATH)
        
        self.system = BlindAssistSystem()

    def process_frame(self, frame):
        """
        Process a single frame: Detect (Dual) -> Estimate -> Draw
        """
        # --- Stream 1: General Obstacles ---
        results_general = self.model_general.track(frame, conf=Config.CONFIDENCE_THRESHOLD, persist=True, verbose=False)
        
        # --- Stream 2: Potholes ---
        # Enable tracking for potholes to allow distance smoothing
        results_pothole = self.model_pothole.track(frame, conf=Config.POTHOLE_CONF_THRESHOLD, persist=True, verbose=False)
        
        # We need to keep track if an alert was triggered in this frame
        alert_triggered = False
        alert_message = ""

        # Get frame width for direction calculation
        frame_width = frame.shape[1]

        # Process General Obstacles
        for result in results_general:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls in Config.TARGET_CLASSES:
                    label = self.model_general.names[cls]
                    obj_id = int(box.id[0]) if box.id is not None else -1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    w = x2 - x1
                    h = y2 - y1
                    center_x = (x1 + x2) / 2
                    direction = self.system.get_direction(center_x, frame_width)
                    
                    raw_dist = self.system.estimate_distance(w, h, cls)
                    
                    if obj_id != -1:
                        dist = self.system.smooth_distance(obj_id, raw_dist)
                    else:
                        dist = raw_dist
                    
                    status, color = self.system.get_warning_level(dist)
                    
                    if not alert_triggered and self.system.should_alert(status):
                        alert_triggered = True
                        # For voice: "Warning: Person, 1.5 meters, straight ahead"
                        alert_message = f"Warning, {label}, {dist} meters, {direction}"
                        self.system.trigger_audio_alert(alert_message)
                        
                    self.draw_box(frame, x1, y1, x2, y2, color, label, dist, status, direction)

        # Process Potholes
        for result in results_pothole:
            boxes = result.boxes
            for box in boxes:
                # Assuming class 0 is 'pothole' in your custom model
                cls = int(box.cls[0])
                obj_id = int(box.id[0]) if box.id is not None else -1
                label = "Pothole"
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                center_x = (x1 + x2) / 2
                direction = self.system.get_direction(center_x, frame_width)
                
                # Pothole distance estimation: Use Ground Plane Logic
                raw_dist = self.system.estimate_distance_ground(y2)
                
                # Apply smoothing if tracked
                if obj_id != -1:
                    dist = self.system.smooth_distance(f"p_{obj_id}", raw_dist)
                else:
                    dist = raw_dist
                
                status, color = self.system.get_warning_level(dist)
                # Override color for Potholes to be distinct (e.g., Purple or Yellow)
                if status == "DANGER": color = (0, 255, 255) # Yellow
                
                if not alert_triggered and self.system.should_alert(status):
                    alert_triggered = True
                    # For voice: "Warning: Pothole, 2.0 meters, at 11 o'clock"
                    alert_message = f"Warning, Pothole, {dist} meters, {direction}"
                    self.system.trigger_audio_alert(alert_message)
                
                self.draw_box(frame, x1, y1, x2, y2, color, label, dist, status, direction)

        return frame, alert_triggered, alert_message

    def draw_box(self, frame, x1, y1, x2, y2, color, label, dist, status, direction):
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Label Background
        text = f"{label} {dist}m {direction}"
        (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
        
        # Label Text
        cv2.putText(frame, text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
