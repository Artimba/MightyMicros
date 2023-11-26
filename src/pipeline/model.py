from ultralytics import YOLO

from src.pipeline.detection import DetectionManager

class Model(object):

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.database = []
        self.manager = DetectionManager()
    
    def predict(self, frame):
        detection_results = self.model(frame)
        frame = self.manager.handle_frame(detection_results[0].boxes, frame)
        # print(detection_results)
        # print(type(detection_results[0].boxes))
        # for i, bbox in enumerate(detection_results[0].boxes.xyxy):
        #     Detection(bbox, detection_results[0].boxes.xyxyn[i], self.database)
        # print('detections: ', len(self.database))
        return frame
        
    
    def track(self, frame):
        return self.model(frame)