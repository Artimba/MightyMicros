from ultralytics import YOLO
import logging
from dataclasses import dataclass, field
from typing import Optional
from ultralytics.engine.results import Boxes
from numpy import ndarray, linalg
from math import atan2, hypot
from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX, line, getTextSize
from torch import equal as tensor_equal
from torch import Tensor
from mmdet.apis import inference_detector


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')

class Model(object):

    def __init__(self, model_path: str):
        self.model = YOLO(model_path) 

        self.manager = DetectionManager()

        
    
    def predict(self, frame):
        logger.debug('Running YOLOv8 inference on the frame')
        
        detection_results = inference_detector(self.model, frame)
        frame = self.model.show_result(frame.copy(), detection_results, show=False)
        frame = self.manager.handle_frame(detection_results[0].boxes, frame)
        print(detection_results)
        print(type(detection_results[0].boxes))
        for i, bbox in enumerate(detection_results[0].boxes.xyxy):
            Detection(bbox, detection_results[0].boxes.xyxyn[i], self.database)

        return self.model(frame, verbose=False)
    

class Detection:
    id: int
    bbox: Tensor
    bbox_norm: Tensor
    

class DetectionManager:
    def __init__(self, frame_rate: int = 30):
        self.detections = {}
        self.next_id = 1
        self.delta_t = frame_rate ** -1
        
    def handle_frame(self, results: Boxes, frame: ndarray) -> ndarray:
        
        frame_detections = []
        
      
        # Generate detections with -1 id for each bbox in results.
        for bbox, bbox_norm in zip(results.xyxy, results.xyxyn):
            frame_detections.append(Detection(-1, bbox, bbox_norm))
      
        
        for detection in frame_detections:
            self.add(detection)
        
        green = (0, 255, 0)
        blue = (255, 0, 0)
        thickness = 2
        font_scale = 0.5

        # Update frame with bboxes that have ids overlayed (inside the bbox).
        for detection in self.detections.values():
            bbox = detection.bbox
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            rectangle(frame, (x1, y1), (x2, y2), color=green, thickness=thickness)  # Draw bbox
            
            label_size, _ = getTextSize(str(detection.id), FONT_HERSHEY_SIMPLEX, font_scale, thickness)

            # Label position (bottom right corner of bbox)
            label_x = x2 + 15
            label_y = y2

            # Check if label would go beyond the frame dimensions
            if label_x + label_size[0] > frame.shape[1]:
                label_x = frame.shape[1] - label_size[0] - 5
            if label_y - label_size[1] < 0:
                label_y = label_size[1] + 5

            # Draw leader line from bbox to text
            line_end_x = label_x if label_x == x2 + 5 else x2
            line_end_y = label_y - label_size[1] // 2
            lineThickness = 2
            line(frame, (x2, y2), (line_end_x, line_end_y), blue, lineThickness)

            # Draw text label
            putText(frame, str(detection.id), (label_x, label_y), FONT_HERSHEY_SIMPLEX, font_scale, blue, thickness)


        
        # Frame updated with bboxs that have id's overlayed (inside the bbox).
        return frame
    
        