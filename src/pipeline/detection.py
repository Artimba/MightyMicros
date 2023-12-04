from dataclasses import dataclass, field
from typing import Optional, Dict
# from ultralytics.engine.results import Boxes
from numpy import ndarray, linalg
from math import atan2, hypot
from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX, line, getTextSize
from torch import equal as tensor_equal
from torch import Tensor

from src.pipeline.kalman import KalmanFilter

def calculate_vector(start: tuple, end: tuple) -> tuple:
    x_1, y_1 = start[:2]
    x_2, y_2 = end[:2]
    
    dx = x_2 - x_1
    dy = y_2 - y_1
    
    angle = atan2(dy, dx) % 360
    distance = hypot(dx, dy)
    
    return distance, angle

def get_direction(angle: float) -> str:

    if 0 <= angle < 45 or 315 <= angle < 360:
        return 'E'
    elif 45 <= angle < 135:
        return 'N'
    elif 135 <= angle < 225:
        return 'W'
    elif 225 <= angle < 315:
        return 'S'
    else:
        return 'E'  # Rut-roh scooby, we got a problem.


@dataclass
class Detection:
    id: int
    bbox: Tensor
    bbox_norm: Tensor
    kalman_filter: KalmanFilter = None
    neighbors: Dict[str, Optional['Detection']] = field(default_factory=lambda: {
        'N': None, 
        'NE': None, 
        'E': None, 
        'SE': None, 
        'S': None, 
        'SW': None, 
        'W': None, 
        'NW': None
    })
    
    def initialize_kalman(self, delta_t: float):
        self.kalman_filter = KalmanFilter(self.bbox_norm, delta_t)
    
    def __eq__(self, __value: object) -> bool:
        
        # Check for bad call.
        if not isinstance(__value, Detection):
            print(f'Type Mismatch: {type(__value)} must be a Detection object')
            return False
        
        # Any match would have same number of neighbors.
        if len(self.neighbors) != len(__value.neighbors):
            return False
        
        threshold = 0.02
        
        # Check if neighbors align.
        for direction, neighbor in self.neighbors.items():
            other_neighbor = __value.neighbors[direction]
            
            if neighbor is None and other_neighbor is None:
                continue
            
            centroid = self.kalman_filter.calculate_centroid(self.bbox_norm)
            other_centroid = __value.kalman_filter.current_state_estimate[:2]
            
            # Compare centroids of neighbors.
            if linalg.norm(centroid - other_centroid) > threshold:
                return False
            
        
        # Neighbors align to other detection. Reasonably assume they are the same.
        return True

class DetectionManager:
    def __init__(self, frame_rate: int = 30):
        self.detections = {}
        self.next_id = 1
        self.delta_t = frame_rate ** -1
        
    def handle_frame(self, results, frame: ndarray) -> ndarray:
        
        frame_detections = []
        
        # Run a prediction on currently managed detections to get estimate locations for this new frame.
        self.predict_detections()
        
        # Generate detections with -1 id for each bbox in results.
        for bbox, bbox_norm in zip(results.xyxy, results.xyxyn):
            frame_detections.append(Detection(-1, bbox, bbox_norm))
        
        for new_detection in frame_detections:
            self.process_detection(new_detection)
        
        
        
        self.generate_neighbors(self.detections.values())
        
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
    
    def generate_neighbors(self, frame_detections):
        # Look at each bbox inside frame_detections. Compare against every other bbox. Use distance and angle (relative to currently processing detection) to calculate neighbors.
        # A single detection should only have a max of 8 detections, one for each direction (N, NE, E, SE, S, SW, W, NW). This check should be done by looking at angle relative to currently detection.
        # N would be 45 - 135 degrees, NE would be 135 - 225 degrees, etc.
        # If a more than one bbox is within a direction, the closest bbox should be used.
        
        for detection in frame_detections:
            neighbors = {'N': None, 'NE': None, 'E': None, 'SE': None,
                         'S': None, 'SW': None, 'W': None, 'NW': None}
            min_distances = {direction: float('inf') for direction in neighbors}
        
            for other_detection in frame_detections:
                if tensor_equal(detection.bbox_norm, other_detection.bbox_norm):
                    # We are at the current detection, so skip.
                    continue
            
                distance, angle = calculate_vector(detection.bbox, other_detection.bbox)
                direction = get_direction(angle)
                
                if distance < min_distances[direction]:
                    min_distances[direction] = distance
                    neighbors[direction] = other_detection
            
            detection.neighbors = neighbors
            
    def process_detection(self, new_detection: Detection):
        # Check if the new detection matches any existing detection
        for _, detection in self.detections.items():
            
            # Compare using neighbors
            if new_detection == detection:
                # Neighbors align. Update the existing detection with the new detection's bbox and bbox_norm.
                detection.bbox = new_detection.bbox
                detection.bbox_norm = new_detection.bbox_norm
                detection.neighbors = new_detection.neighbors
                # Update Kalman Filter with new measurement
                detection.kalman_filter.update(new_detection.bbox_norm)
                return

        # If no match is found, initialize a new detection.
        self.add(new_detection)
    
    def add(self, new_detection: Detection):
        """Do not call this independently. Use `:meth: process_detection()` instead.

        Args:
            new_detection (Detection): Detection geneated from a new frame.
        """
        new_detection.initialize_kalman(self.delta_t)
        new_detection.id = self.next_id
        self.detections[self.next_id] = new_detection
        self.next_id += 1
    
    def predict_detections(self):
        for _, detection in self.detections.items():
            if detection.kalman_filter is not None:
                detection.kalman_filter.predict()
    
    # def update_detections(self, frame_detections: list[Detection]):
    #     for new_detection in frame_detections:
    #         is_match = False
    #         for _, existing_detection in self.detections.items():
    #             if new_detection == existing_detection:
    #                 existing_detection.update(new_detection.bbox_norm)
    #                 is_match = True
    #                 break
                
    #             if not is_match:
    #                 new_detection.initialize_kalman(self.delta_t)
    #                 new_detection.id = self.next_id
    #                 self.detections[self.next_id] = new_detection
    #                 self.next_id += 1
                    
    # def add(self, new_detection: Detection):
        
    #     for _, detection in self.detections.items():
    #         if new_detection == detection:
    #             print("Found a match!")
    #             detection.bbox = new_detection.bbox
    #             detection.bbox_norm = new_detection.bbox_norm
    #             detection.neighbors = new_detection.neighbors
    #             return
        
    #     print("Generating new id")
    #     new_detection.id = self.next_id
    #     self.detections[self.next_id] = new_detection
    #     self.next_id += 1