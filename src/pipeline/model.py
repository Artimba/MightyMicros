# from ultralytics import YOLO
from pathlib import Path
import torch
import mmcv
from mmdet.apis import inference_detector, init_detector

from src.pipeline.detection import DetectionManager
from src import PROJECT_ROOT

class Model(object):

    def __init__(self, model: str = 'latest.pth'):
        # self.model = YOLO(model_path)
        # self.model = torch.hub.load('/home/sky/yolov5_obb', 'custom', path='/home/sky/yolov5_obb/runs/train/exp26/weights/best.pt', source='local')
        self.cfg = mmcv.Config.fromfile(Path(PROJECT_ROOT, 'pipeline', 'configs', 'oriented_rcnn_r50_fpn_1x_dota_le90.py'))
        self.cfg.dataset_type = 'MIGHTYDataset'
        self.cfg.data_root = '/home/sky/datasets/obb_split/'

        self.cfg.data.test.type = 'MIGHTYDataset'
        self.cfg.data.test.data_root = '/home/sky/datasets/obb_split/'
        self.cfg.data.test.ann_file = 'val'
        self.cfg.data.test.img_prefix = 'images'

        self.cfg.data.train.type = 'MIGHTYDataset'
        self.cfg.data.train.data_root = '/home/sky/datasets/obb_split/'
        self.cfg.data.train.ann_file = 'train'
        self.cfg.data.train.img_prefix = 'images'

        self.cfg.data.val.type = 'MIGHTYDataset'
        self.cfg.data.val.data_root = '/home/sky/datasets/obb_split/'
        self.cfg.data.val.ann_file = 'val'
        self.cfg.data.val.img_prefix = 'images'
        self.cfg.model.roi_head.bbox_head.num_classes = 1
        
        self.model_checkpoint = Path(PROJECT_ROOT, 'pipeline', 'weights', model)
        self.model = init_detector(self.cfg, self.model_checkpoint, device='cuda:0')
        
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
    
