"""
This class gets ran server-side for the label-studio ML backend. There shouldn't be any need to interact with this.
"""

from label_studio_ml.model import LabelStudioMLBase
import cv2
import numpy as np
from ultralytics import YOLO

class YOLOModel(LabelStudioMLBase):

    def __init__(self, **kwargs):
        super(YOLOModel, self).__init__(**kwargs)
        
        self.from_name = "box"
        self.to_name = "video"
        self.labels = ["slice"]
        
        # Load YOLO model here (weights, cfg, etc.)
        self.model = YOLO("yolov8m.pt")
        self.model.eval()
        
        from_name, schema = list(self.parsed_label_config.items())[0]
        self.from_name = from_name
        self.to_name = schema['to_name'][0]
        self.labels = schema['labels']
        
    def predict(self, tasks, **kwargs):
        predictions = []
        
        for task in tasks:
            video_path = task["data"]["video"]
            video = cv2.VideoCapture(video_path)
            frame_rate = video.get(cv2.CAP_PROP_FPS)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Skip every 3nd frame for a 30fps video (resulting in processing 10fps)
            skip_frames = 3
            
            for i in range(0, total_frames, skip_frames):
                video.set(cv2.CAP_PROP_POS_FRAMES, i)
                status, frame = video.read()

                # If frame reading was successful, process it
                if status:
                    # Get YOLO predictions
                    yolo_predictions = self.model.predict(frame)

                    # Convert YOLO predictions to Label Studio format
                    formatted_predictions = self.format_predictions(yolo_predictions)

                    predictions.append(formatted_predictions)

            video.release()
            
        return predictions

    def format_predictions(self, yolo_predictions):
        formatted_predictions = {
            'result': [],
            'from_name': self.from_name,
            'to_name': self.to_name,
            'type': 'rectanglelabels'
        }
        
        for pred in yolo_predictions:
            formatted_predictions['result'].append({
                'id': str(np.random.randint(1000000)),
                'original_width': pred['bbox'][2],
                'original_height': pred['bbox'][3],
                'value': {
                    'rectanglelabels': [pred['label']],
                    'x': pred['bbox'][0],
                    'y': pred['bbox'][1],
                    'width': pred['bbox'][2],
                    'height': pred['bbox'][3]
                }
            })
            
        return [formatted_predictions]