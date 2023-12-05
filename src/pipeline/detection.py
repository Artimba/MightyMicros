from ultralytics import YOLO
import logging
from ultralytics.engine.results import Boxes
from numpy import ndarray, linalg
from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX, line, getTextSize
from torch import Tensor

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')

class Model(object):

    def __init__(self, model_path: str):
        self.model = YOLO(model_path) 

        self.manager = DetectionManager()
    
    def predict(self, frame):
        logger.debug('Running YOLOv8 inference on the frame')
        return self.model(frame, verbose=False)
    
        