from ultralytics import YOLO
from pathlib import Path
def main():
    # Load a model
    model = YOLO("A:/MightyMicros/src/pipeline/weights/best.pt")  # load a pretrained model (recommended for training)

    # Use the model
    model.train(data="A:/MightyMicros/src/pipeline/configs/mighty_tracking.yaml", epochs=300)  # train the model
    metrics = model.val()  # evaluate model performance on the validation set
    val_images_path = Path("A:/MightyMicros/datasets/training/images")
    test_image = next(val_images_path.glob('frame_*.jpg'))  # This gets the first JPEG image in the directory
    results = model.predict(str(test_image))
    path = model.export(format="onnx")  # export the model to ONNX format

if __name__ == '__main__':
    main()