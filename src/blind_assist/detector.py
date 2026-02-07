import cv2
from ultralytics import YOLO
from .config import Config
from .core import BlindAssistSystem

class Detector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.system = BlindAssistSystem()

    def process_frame(self, frame):
        """
        Process a single frame: Detect -> Estimate -> Draw
        """
        # Run inference (enable tracking for ID consistency)
        results = self.model.track(frame, conf=Config.CONFIDENCE_THRESHOLD, persist=True, verbose=False)
        
        # We need to keep track if an alert was triggered in this frame
        alert_triggered = False
        alert_message = ""

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                
                # Filter for target classes
                if cls in Config.TARGET_CLASSES:
                    label = self.model.names[cls]
                    
                    # Get ID if available (for tracking/smoothing)
                    obj_id = int(box.id[0]) if box.id is not None else -1
                    
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # 1. Estimate Distance (Class-Specific)
                    h = y2 - y1
                    raw_dist = self.system.estimate_distance(h, cls)
                    
                    # Apply Smoothing if we have an ID
                    if obj_id != -1:
                        dist = self.system.smooth_distance(obj_id, raw_dist)
                    else:
                        dist = raw_dist
                    
                    # 2. Get Status
                    status, color = self.system.get_warning_level(dist)
                    
                    # 3. Check for Alert (only first critical alert per frame to avoid spam)
                    if not alert_triggered and self.system.should_alert(status):
                        alert_triggered = True
                        alert_message = f"Warning: {label} {dist}m"
                        
                    # 4. Draw UI
                    self.draw_box(frame, x1, y1, x2, y2, color, label, dist, status)

        return frame, alert_triggered, alert_message

    def draw_box(self, frame, x1, y1, x2, y2, color, label, dist, status):
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Label Background
        text = f"{label} {dist}m"
        (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
        
        # Label Text
        cv2.putText(frame, text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
