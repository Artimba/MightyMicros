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
from PyQt5.QtWidgets import QTextEdit


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')

class Model(object):

    def __init__(self, model_path: str, output1: QTextEdit, output2: QTextEdit):
        self.model = YOLO(model_path) 

        self.manager = DetectionManager(30, output1, output2)
      

        
    
    def predict(self, frame):
        logger.debug('Running YOLOv8 inference on the frame')
        
        detection_results = self.model(frame, verbose = False)
        #frame = self.model.show_result(frame.copy(), detection_results, show=False)
        frame = detection_results[0].plot(labels=False, masks=False)
        frame = self.manager.handle_frame(detection_results[0].boxes, frame)
        #print(detection_results)
        #print(type(detection_results[0].boxes))
        #for i, bbox in enumerate(detection_results[0].boxes.xyxy):
            #Detection(bbox, detection_results[0].boxes.xyxyn[i], self.database)

        return frame, detection_results

        

    #def track(self, frame):
     #   return self.model(frame, verbose=False)
    

class Detection:
    def __init__(self, id: int, bbox: Tensor, bbox_norm: Tensor):
        self.id = id 
        self.bbox = bbox
        self.bbox_norm = bbox_norm

    

class DetectionManager:
    def __init__(self, frame_rate: int, output1: QTextEdit, output2: QTextEdit):
        self.detections = {}
        self.next_id = 1
        self.delta_t = frame_rate ** -1
        self.prevDetectionLength = 0
        self.output1 = output1 
        self.output2 = output2

        #self.lastSliceNum = 1
        
    def handle_frame(self, results: Boxes, frame: ndarray) -> ndarray:
        
        frame_detections = []
        slice_num = 1
        
        
        # Generate detections with -1 id for each bbox in results.
        for bbox, bbox_norm in zip(results.xyxy, results.xyxyn):
            frame_detections.append(Detection(slice_num, bbox, bbox_norm))
            slice_num += 1
      
        
        #for detection in frame_detections:
         #   self.add(detection)
        
        green = (0, 255, 0)
        blue = (255, 0, 0)
        thickness = 2
        font_scale = 0.5

        # Update frame with bboxes that have ids overlayed (inside the bbox).
        
        for detection in frame_detections:
            bbox = detection.bbox
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            frame = rectangle(frame, (x1, y1), (x2, y2), color=green, thickness=thickness)  # Draw bbox
            
            
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
            frame = line(frame, (x2, y2), (line_end_x, line_end_y), blue, lineThickness)

            # Draw text label
            frame = putText(frame, str(detection.id), (label_x, label_y), FONT_HERSHEY_SIMPLEX, font_scale, blue, thickness)

            
        if len(frame_detections) > self.prevDetectionLength:
            num_slices = len(frame_detections) - self.prevDetectionLength
            for i in range(1, num_slices+1): #trying this out
                
                self.output1.append("Slice " + str(self.prevDetectionLength + i) + " detected" )
                self.output2.append("Slice " + str(self.prevDetectionLength + i) + " detected" )


            self.prevDetectionLength = len(frame_detections)


        
        # Frame updated with bboxs that have id's overlayed (inside the bbox).
        return frame
    
        