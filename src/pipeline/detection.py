from ultralytics import YOLO

class Model(object):

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
    
    def predict(self, frame):
        return self.model(frame)
        