from ultralytics import YOLO

def train():
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    # Note: You need a dataset.yaml file describing your pothole dataset
    # We assume 'data/pothole.yaml' exists or you will provide one.
    results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
    
    # Validation
    metrics = model.val()
    
    # Export
    success = model.export(format="onnx")

if __name__ == '__main__':
    train()
