from ultralytics import YOLO
import logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')

class Model(object):

    def __init__(self, model_path: str):
        self.model = YOLO(model_path) 
    
    def predict(self, frame):
        logger.debug('Running YOLOv8 inference on the frame')
        return self.model(frame, verbose=False)
        