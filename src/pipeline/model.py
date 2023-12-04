# from ultralytics import YOLO
from pathlib import Path
import torch
import mmcv
from mmcv.runner import load_checkpoint
from mmdet.apis import inference_detector, show_result_pyplot
from mmrotate.models import build_detector

from src.pipeline.detection import DetectionManager
from src import PROJECT_ROOT

class Model(object):

    def __init__(self, model: str = 'latest.pth'):
        # # self.model = YOLO(model_path)
        # # self.model = torch.hub.load('/home/sky/yolov5_obb', 'custom', path='/home/sky/yolov5_obb/runs/train/exp26/weights/best.pt', source='local')
        
        # self.cfg = mmcv.Config.fromfile(str(Path(PROJECT_ROOT, 'pipeline', 'configs', 'oriented_rcnn_r50_fpn_1x_dota_le90.py')))
        # self.cfg = mmcv.Config.fromfile(PROJECT_ROOT + '\oriented_rcnn_r50_fpn_1x_dota_le90.py')
        # self.cfg.model.pretrained = None
        # self.cfg.dataset_type = 'MIGHTYDataset'
        # # self.cfg.data_root = '/home/sky/datasets/obb_split/'

        # # self.cfg.data.test.type = 'MIGHTYDataset'
        # # self.cfg.data.test.data_root = '/home/sky/datasets/obb_split/'
        # # self.cfg.data.test.ann_file = 'val'
        # # self.cfg.data.test.img_prefix = 'images'

        # self.cfg.model.roi_head.bbox_head.num_classes = 1
        # if torch.cuda.is_available():
        #     self.device = 'cuda:0'
        # else:
        #     self.device = None
        
        # model_checkpoint_path = Path(PROJECT_ROOT, 'pipeline', 'weights', model)
        # if torch.cuda.is_available():
        #     self.model_checkpoint = load_checkpoint(self.cfg, str(model_checkpoint_path))
        # else:
        #     self.model_checkpoint = load_checkpoint(self.cfg, str(model_checkpoint_path), map_location='cpu')

        # self.model = build_detector(self.cfg, self.model_checkpoint)
        
        # if torch.cuda.is_available():
        #     self.model.to(self.device)
        
        # self.model.eval()
        
        # Choose to use a config and initialize the detector
        config = str(Path(PROJECT_ROOT, 'pipeline', 'configs', 'oriented_rcnn_r50_fpn_1x_dota_le90.py'))
        # Setup a checkpoint file to load
        checkpoint = str(Path(PROJECT_ROOT, 'pipeline', 'weights', model))

        # Set the device to be used for evaluation
        if torch.cuda.is_available():
            device = 'cuda:0'
        else:
            device='cpu'

        # Load the config
        config = mmcv.Config.fromfile(config)
        config.model.roi_head.bbox_head.num_classes = 1
        config.dataset_type = 'MIGHTYDataset'
        
        # Set pretrained to be None since we do not need pretrained model here
        config.model.pretrained = None

        # Initialize the detector
        self.model = build_detector(config.model)

        # Load checkpoint
        checkpoint = load_checkpoint(self.model, checkpoint, map_location=device)

        # Set the classes of models for inference
        self.model.CLASSES = checkpoint['meta']['CLASSES']

        # We need to set the model's cfg for inference
        self.model.cfg = config

        # Convert the model to GPU
        if torch.cuda.is_available():
            self.model.to(device)
        # Convert the model into evaluation mode
        self.model.eval()
        
        self.database = []
        self.manager = DetectionManager()
    
    def predict(self, frame):
        detection_results = inference_detector(self.model, frame)
        frame = self.model.show_result(frame.copy(), detection_results, show=False)
        # frame = self.manager.handle_frame(detection_results[0].boxes, frame)
        # print(detection_results)
        # print(type(detection_results[0].boxes))
        # for i, bbox in enumerate(detection_results[0].boxes.xyxy):
        #     Detection(bbox, detection_results[0].boxes.xyxyn[i], self.database)
        # print('detections: ', len(self.database))
        return frame
        
    
    def track(self, frame):
        return self.model(frame)
    
