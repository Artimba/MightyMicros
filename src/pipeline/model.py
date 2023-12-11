# from ultralytics import YOLO
from pathlib import Path
import importlib.resources as pkg
import cv2
import torch
import mmcv
from mmcv.runner import load_checkpoint
from mmdet.apis import inference_detector, show_result_pyplot
from mmrotate.models import build_detector

from src.pipeline.detection import DetectionManager
from src import PROJECT_ROOT
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Detection_Model')
class Model(object):

    def __init__(self, model: str = 'model.pth'):      
        # Choose to use a config and initialize the detector
        # config = str(Path(PROJECT_ROOT, 'pipeline', 'configs', 'oriented_rcnn_r50_fpn_1x_dota_le90.py'))
        with pkg.path('src.pipeline.configs', 'oriented_rcnn_r50_fpn_1x_dota_le90.py') as config_path:
            if config_path.exists():
                config = config_path
            else:
                logger.info(f"Config file not found at path {config_path}.")
                return
        # Setup a checkpoint file to load
        # checkpoint = str(Path(PROJECT_ROOT, 'pipeline', 'weights', model))
        with pkg.path('src.pipeline.weights', model) as model_path:
            if model_path.exists():
                mighty_model = str(model_path)
            else:
                logger.info(f"Model binary not found at path {model_path}.")
                return
        print(mighty_model)
        # Set the device to be used for evaluation
        if torch.cuda.is_available():
            print("CUDA Discovered.")
            self.device = 'cuda:0'
        else:
            print("CUDA Not Found. Attempting CPU")
            self.device='cpu'

        # Load the config
        config = mmcv.Config.fromfile(config)
        config.model.roi_head.bbox_head.num_classes = 1
        config.dataset_type = 'MIGHTYDataset'
        
        # Set pretrained to be None since we do not need pretrained model here
        config.model.pretrained = None

        # Initialize the detector
        self.model = build_detector(config.model)

        # Load checkpoint
        checkpoint = load_checkpoint(self.model, mighty_model, map_location=self.device)

        # Set the classes of models for inference
        self.model.CLASSES = checkpoint['meta']['CLASSES']

        # We need to set the model's cfg for inference
        self.model.cfg = config

        # Convert the model to GPU
        # if torch.cuda.is_available():
        self.model.to(self.device)
        # Convert the model into evaluation mode
        self.model.eval()
        
        self.database = []
        self.manager = DetectionManager()
        
        self.frame_count = 0
    
    def predict(self, frame):
        frame = cv2.resize(frame, (640, 480))
        if self.frame_count % 10 == 0:
            detection_results = inference_detector(self.model, frame)
            frame = self.manager.handle_detect(detection_results, frame)
        else:
            frame = self.manager.handle_track(frame)
        self.frame_count += 1
        return frame
        
    
    def track(self, frame):
        return self.model(frame)
    
