from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
import torch
from ultralytics.engine.results import Boxes, Results
from math import atan2, hypot
import cv2
from torch import equal as tensor_equal
from torch import Tensor
import numpy as np
from matplotlib import pyplot as plt

from src.pipeline.kalman import KalmanFilter

EPS = 1e-2 # Epsilon value for matplotlib scale wiggling
EPS2 = 1e-5 # Epsilon value for numpy.isclose()
MIN_AREAS = 800 # Lower bound of scales
MAX_AREAS = 30000 # Upper bound of scales
COORDINATES = 9 # Amount of coordinates in a bounding box + score

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
    bbox: Union[Tensor, np.ndarray]
    bbox_norm: Union[Tensor, np.ndarray]
    xywh: Union[Tensor, np.ndarray] = None
    centroid_norm: Union[Tensor, np.ndarray] = None
    score: Union[Tensor, float] = None
    kalman_filter: KalmanFilter = None
    neighbors: Dict[str, Optional['Detection']] = field(default_factory=lambda: {
        'N': None, 
        'NE': None, 
        'E': None, 
        'SE': None, 
        'S': None, 
        'SW': None, 
        'W': None, 
        'NW': None})
    
    def initialize_kalman(self, delta_t: float):
        self.kalman_filter = KalmanFilter(self.bbox_norm, delta_t)
    
    def convert_tensor_to_numpy(self):
        if isinstance(self.bbox, Tensor):
            self.bbox = self.bbox.numpy()
        if isinstance(self.bbox_norm, Tensor):
            self.bbox_norm = self.bbox_norm.numpy()
        if isinstance(self.xywh, Tensor):
            self.xywh = self.xywh.numpy()
        if isinstance(self.centroid_norm, Tensor):
            self.centroid_norm = self.centroid_norm.numpy()
        if isinstance(self.score, Tensor):
            self.score = self.score.item()
    
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
            if np.linalg.norm(centroid - other_centroid) > threshold:
                return False
            
        
        # Neighbors align to other detection. Reasonably assume they are the same.
        return True

class DetectionManager:
    def __init__(self, frame_rate: int = 30):
        self.detections = {}
        self.next_id = 1
        self.delta_t = frame_rate ** -1
        
    def handle_frame(self, results: Union[Results, np.ndarray], frame: np.ndarray) -> np.ndarray:
        self.detections = {} # TODO: TEMPORARY
        self.next_id = 1 # TODO: TEMPORARY
        
        frame_detections = []
        self.predict_detections()
        
        # if isinstance(results, Results):
        #     # Convert to generic format.
        #     bboxes = self.convert_yolo_to_generic(results)
        #     for bbox, bbox_norm, xywh, centroid_norm, score in bboxes:
        #         frame_detections.append(Detection(id=-1, 
        #                                         bbox=bbox, 
        #                                         bbox_norm=bbox_norm, 
        #                                         score=score, 
        #                                         xywh=xywh,
        #                                         centroid_norm=centroid_norm))
        # else:
        #     bboxes, bbox_norms = self.handle_results(results, (frame.shape[1], frame.shape[0]))
        #     for i in range(len(bboxes)):
        #         centroid = results[0][i, 0:2]
        #         centroid_norm = np.array([centroid[0] / frame.shape[1], centroid[1] / frame.shape[0]])
        #         frame_detections.append(Detection(id=-1, 
        #                                         bbox=bboxes[i, 0:8], 
        #                                         bbox_norm=bbox_norms[i, 0:8], 
        #                                         score=bboxes[i, 8], 
        #                                         xywh=results[0][i, 0:4],
        #                                         centroid_norm=centroid_norm))
        for bbox, bbox_norm in zip(results.boxes.xyxy, results.boxes.xyxyn):
            frame_detections.append(Detection(-1, bbox, bbox_norm))
            
        
        
        # Run a prediction on currently managed detections to get estimate locations for this new frame.
        
        
        # Generate detections with -1 id for each bbox in results.

        
        for new_detection in frame_detections:
            self.process_detection(new_detection)
        
        self.generate_neighbors(self.detections.values())
        
        for detection in frame_detections:
            self.add(detection)
        
        green = (0, 255, 0)
        blue = (255, 0, 0)
        thickness = 2
        font_scale = 0.5

        # frame = self.draw_bboxes(frame, color=(125, 43, 250), thickness=thickness, font_size=font_scale)
        # Use cv2 to draw the bounding boxes
        for detection in self.detections.values():
            bbox = detection.bbox
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color=green, thickness=thickness)  # Draw bbox
            
            # # Draw the id
            # centroid = detection.kalman_filter.calculate_centroid(detection.bbox_norm)
            # centroid = centroid.astype(np.int32)
            # cv2.putText(frame, str(detection.id), (centroid[0], centroid[1]), cv2.FONT_HERSHEY_SIMPLEX, font_scale, blue, thickness)
        
        # Frame updated with bboxs that have id's overlayed (inside the bbox).
        return frame
    
    def generate_neighbors(self, frame_detections: List[Detection]):
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
    
    def convert_yolo_to_generic(self, yolo_results: Results):
        boxes_obj = yolo_results.boxes  # Extract the Boxes object
        xywh = boxes_obj.xywh  # Bounding boxes (center_x, center_y, width, height)
        xywhn = boxes_obj.xywhn  # Normalized bounding boxes
        xyxy = boxes_obj.xyxy  # Bounding boxes (x1, y1, x2, y2)
        xyxyn = boxes_obj.xyxyn  # Normalized bounding boxes (x1, y1, x2, y2)
        conf = boxes_obj.conf  # Confidence scores
        orig_shape = boxes_obj.orig_shape  # Original shape of the image

        # Image dimensions
        image_height, image_width = orig_shape

        # Conversion
        converted_boxes = []
        for i in range(len(conf)):
            # Extract the bounding box and score
            box = xywh[i]
            score = conf[i]  # Keep it as a tensor
            
            # Convert to bbox (tensor operations)
            top_left = box[:2] - box[2:] / 2
            bottom_right = box[:2] + box[2:] / 2
            bbox = torch.cat((top_left, bottom_right), dim=0)
            
            # Convert to bbox_normalized (tensor operations)
            scale = torch.tensor([image_width, image_height, image_width, image_height], dtype=torch.float32)
            bbox_normalized = bbox / scale
            
            # Centroid normalized (tensor operations)
            centroid_norm = xywhn[i][:2]
            
            converted_boxes.append((bbox, bbox_normalized, box, centroid_norm, score))

        return converted_boxes

    def handle_results(self, results, frame_size: tuple) -> tuple:
        """Convert results from MMCV to a tuple of bounding boxes and labels.
        
        This method incorporates modifications based on code from the mmrotate repository (OpenMMLab), 
        available at [https://github.com/open-mmlab/mmrotate]. mmrotate is distributed under the Apache 2.0 License.

        Args:
            results: The detection results from inference.
            frame_size (tuple): The size of the frame (width, height).

        Returns:
            Tuple: A tuple containing two lists - the first with un-normalized bounding boxes, 
                and the second with normalized bounding boxes.
        """
        if isinstance(results, tuple):
            bbox_result, segm_result = results
            if isinstance(segm_result, tuple):
                segm_result = segm_result[0]
        else:
            bbox_result, segmn_result = results, None
        
        bboxes = np.vstack(bbox_result)
        
        # labels = [
        #     np.full(bbox.shape[0], i, dtype=np.int32)
        #     for i, bbox in enumerate(bbox_result)
        # ]
        # labels = np.concatenate(labels)
        
        # Normalize bounding boxes
        img_width, img_height = frame_size
        bboxes_coordinates = np.zeros((bboxes.shape[0], COORDINATES), dtype=np.float32)
        for i, bbox in enumerate(bboxes):
            x_center, y_center, width, height, rotation = bbox[:5]
            half_width_x, half_width_y = width / 2 * np.cos(rotation), width / 2 * np.sin(rotation)
            half_height_x, half_height_y = -height / 2 * np.sin(rotation), height / 2 * np.cos(rotation)
            
            p1 = (x_center - half_width_x - half_height_x, y_center - half_width_y - half_height_y)
            p2 = (x_center + half_width_x - half_height_x, y_center + half_width_y - half_height_y)
            p3 = (x_center + half_width_x + half_height_x, y_center + half_width_y + half_height_y)
            p4 = (x_center - half_width_x + half_height_x, y_center - half_width_y + half_height_y)
            
            bboxes_coordinates[i, 0] = p1[0]  # x1
            bboxes_coordinates[i, 1] = p1[1]  # y1
            bboxes_coordinates[i, 2] = p2[0]  # x2
            bboxes_coordinates[i, 3] = p2[1]  # y2
            bboxes_coordinates[i, 4] = p3[0]  # x3
            bboxes_coordinates[i, 5] = p3[1]  # y3
            bboxes_coordinates[i, 6] = p4[0]  # x4
            bboxes_coordinates[i, 7] = p4[1]  # y4     
                 
            # Copy over score
            bboxes_coordinates[i, 8] = bbox[5]
            
        
        normalized_bboxes = np.zeros_like(bboxes_coordinates, dtype=np.float32)
        normalized_bboxes[:, [0, 2, 4, 6]] = bboxes_coordinates[:, [0, 2, 4, 6]] / img_width
        normalized_bboxes[:, [1, 3, 5, 7]] = bboxes_coordinates[:, [1, 3, 5, 7]] / img_height

        # Copy over score
        normalized_bboxes[:, 8] = bboxes_coordinates[:, 8]
        

        return (bboxes_coordinates, normalized_bboxes)

    def draw_bboxes(self, frame: np.ndarray, color=(0,255,0), thickness=2, alpha=0.5, font_size=13) -> np.ndarray:
        width, height = frame.shape[1], frame.shape[0]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.ascontiguousarray(frame)
        fig, ax = plt.subplots(frameon=False)
        canvas = fig.canvas
        dpi = fig.get_dpi()
        fig.set_size_inches((width + EPS) / dpi, (height + EPS) / dpi)
        # plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax.axis('off')

        positions_list = []
        areas_list = []

        for detection in self.detections.values():
            detection.convert_tensor_to_numpy()
            bbox = detection.bbox.astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [bbox], isClosed=True, color=color, thickness=thickness)

            posi = detection.xywh[:2].astype(np.int32) + thickness
            positions_list.append(posi)

            area = (detection.xywh[3] - detection.xywh[1]) * (detection.xywh[2] - detection.xywh[0])
            areas_list.append(area)

        positions = np.array(positions_list)
        areas = np.array(areas_list)
        scales = 0.5 + (areas - MIN_AREAS) / (MAX_AREAS - MIN_AREAS)
        scales = np.clip(scales, 0.5, 1.0)

        for i, (pos, detection) in enumerate(zip(positions, self.detections.values())):
            label_text = f'{detection.id} | '
            if detection.score is not None:
                truncated_score = (detection.score * 100) // 1 / 100
                label_text += f'{truncated_score:.02f}'
            font_size_mask = font_size if scales is None else font_size * scales[i]
            ax.text(pos[0], pos[1], f'{label_text}', 
                    bbox={
                        'facecolor': 'black',
                        'alpha': 0.8,
                        'pad': 0.7,
                        'edgecolor': 'none'
                    },
                    color='w', 
                    fontsize=font_size_mask,
                    verticalalignment='top',
                    horizontalalignment='left')

        ax.imshow(frame)
        
        stream, _ = canvas.print_to_buffer()
        buffer = np.frombuffer(stream, dtype='uint8')
        img_rgba = buffer.reshape(height, width, 4)
        rgb, alpha = np.split(img_rgba, [3], axis=2)
        frame = rgb.astype('uint8')
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        plt.close(fig)
        
        return frame