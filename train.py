from ultralytics import YOLO
from pathlib import Path

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="mighty_tracking.yaml", epochs=3)  # train the model
metrics = model.val()  # evaluate model performance on the validation set
val_images_path = Path("training/images/val")
test_image = next(val_images_path.glob('frame_*.jpg'))  # This gets the first JPEG image in the directory
results = model.predict(str(test_image))
path = model.export(format="onnx")  # export the model to ONNX format