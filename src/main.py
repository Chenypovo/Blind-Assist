import cv2
import argparse
import sys
import os
from blind_assist.detector import Detector

def main():
    parser = argparse.ArgumentParser(description="Blind Assist: AI-Powered Obstacle Detection")
    parser.add_argument("--source", type=str, default="0", help="Path to input video file or camera index (default: 0)")
    parser.add_argument("--output", type=str, default="output.mp4", help="Filename for output video (saved in output/ folder)")
    parser.add_argument("--headless", action="store_true", help="Run without GUI (Output file only)")
    parser.add_argument("--model", type=str, default="models/yolov8n.pt", help="YOLO model path")
    
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, args.output)

    # Determine if source is a file or a camera index
    try:
        source = int(args.source)
        is_camera = True
    except ValueError:
        source = args.source
        is_camera = False

    if not is_camera and not os.path.exists(source):
        print(f"Error: Source file '{source}' not found.")
        sys.exit(1)

    print(f"Initializing Blind Assist...")
    print(f"Source: {source} ({'Camera' if is_camera else 'File'})")
    print(f"Output: {output_path}")
    print(f"Mode: {'Headless' if args.headless else 'GUI'}")

    detector = Detector(model_path=args.model)
    cap = cv2.VideoCapture(source)
    
    # Video Writer Setup
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = int(cap.get(cv2.CAP_PROP_FPS))
    if fps <= 0: fps = 30 # Default for camera
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processing frame {frame_count}...", end='\r')

        # Core Processing
        processed_frame, alert, msg = detector.process_frame(frame)
        
        if alert:
            print(f"\n[ALERT] {msg}")

        # Write to file
        out.write(processed_frame)

        # GUI Display (only if not headless)
        if not args.headless:
            cv2.imshow("Blind Assist Demo", processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\nDone! Output saved to: {args.output}")

if __name__ == "__main__":
    main()
