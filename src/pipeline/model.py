from ultralytics import YOLO

from src.pipeline.detection import Detection

class Model(object):

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.database = []
    
    def predict(self, frame):
        detection_results = self.model(frame)
        # print(detection_results)
        for i, bbox in enumerate(detection_results[0].boxes.xyxy):
            Detection(bbox, detection_results[0].boxes.xyxyn[i], self.database)
        print('detections: ', len(self.database))
        return detection_results
        
    
    def track(self, frame):
        return self.model(frame)