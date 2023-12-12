# from ultralytics import YOLO
from ultralytics import YOLO
import importlib.resources as pkg
import logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')

from src.pipeline.detection import DetectionManager

class Model(object):

    def __init__(self, model: str = 'model.pt'):
        with pkg.path('src.pipeline.weights', model) as model_path:
            if model_path.exists():
                mighty_model = str(model_path)
            else:
                logger.info(f"Model binary not found at path {model_path}.")
                return
        print(mighty_model)
        self.model = YOLO(mighty_model)
        self.manager = DetectionManager()
    
    def predict(self, frame):
        logger.debug('Running YOLOv8 inference on the frame')
        results = self.model(frame, verbose=False)
        frame = self.manager.handle_frame(results[0], frame)
        return frame
        
        