# Blind Assist 🦇

**AI-powered Obstacle Detection for the Visually Impaired**

> "A Second Pair of Eyes" - Real-time detection of ground and dynamic obstacles.

## 🚀 Features

*   **Real-time Detection**: Uses YOLOv8 (Nano) for fast inference.
*   **Monocular Distance Estimation**: Approximates distance based on object size.
*   **Smart Alerts**: Audio warnings for "DANGER" (<1.5m) zones with cooldown logic.
*   **Headless Mode**: Run on servers without GUI.

## 🛠 Installation

```bash
pip install ultralytics opencv-python
```

## 🏃 Usage

**Run on a video file:**

```bash
python src/main.py --source data/test_video.mp4 --output output/result.mp4 --headless
```

**Live Demo (Webcam):**

```bash
python src/main.py --source 0
```

## 📂 Project Structure

*   `src/blind_assist/`: Core logic and config.
*   `data/`: Test videos and images.
*   `models/`: YOLO weights.

## 📜 License

MIT
