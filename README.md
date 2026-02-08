# Blind Assist 🦐🦇

**AI-powered Obstacle & Pothole Detection with Spatial Audio Feedback**

> "A Second Pair of Eyes" — Real-time detection, monocular distance estimation, and spatial alerts for urban navigation.

---

## 📺 Demo & Audio Feedback

![Detection Preview](https://github.com/Chenypovo/Blind-Assist/blob/main/output/demo_preview.gif?raw=true)

**🔈 Real-time Audio Alerts:**
The system doesn't just draw boxes; it talks to you. Using macOS native TTS, it provides critical information:
> *"Warning: Person, 1.2 meters, straight ahead"*
> *"Warning: Pothole, 0.8 meters, at 11 o'clock"*

## 🚀 Key Features

*   **Dual-Model Architecture**: 
    *   **YOLOv8n**: Real-time detection of 16+ urban classes (People, Cars, Bikes, Lights, etc.).
    *   **Pothole Expert**: Custom-trained model specialized in detecting road hazards and potholes.
*   **Spatial Navigation (O'Clock Method)**: Provides directions in a "clock" format (10, 11, 12, 1, 2 o'clock) for precise orientation.
*   **W+H Distance Fusion**: Improved monocular depth estimation combining both object width and height for stability.
*   **Adaptive Ground Mapping**: Dynamic horizon-based distance estimation for ground-level obstacles.
*   **Mac-Ready**: Optimized for Mac cameras and native `say` command integration.

## 🛠 Installation

```bash
# Clone the repo
git clone https://github.com/Chenypovo/Blind-Assist.git
cd Blind-Assist

# Install dependencies
pip install ultralytics opencv-python
```

## 🏃 Usage

### 📷 Live Mode (Webcam)
```bash
python src/main.py --source 0
```

### 🎞 Video Processing (with H.264 export)
```bash
python src/main.py --source data/videos/test_video.mp4 --output urban_test.mp4
```

## 📂 Project Structure

*   `src/blind_assist/`: Core logic, Config, and Distance Estimation.
*   `models/`: Pre-trained YOLOv8 and Pothole-specific weights.
*   `data/`: Sample urban videos for testing.
*   `output/`: Processed videos with overlays and audit logs.

## 📅 Roadmap
- [x] Dual-model parallel inference.
- [x] Spatial audio alerts (Clock method).
- [x] H.264 video encoding for Mac compatibility.
- [ ] Integration with Depth-Anything-V2 for dense depth maps.
- [ ] iOS/Android deployment research.

## 📜 License

MIT License. Developed by **cyp**.
