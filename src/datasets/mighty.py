from mmrotate.datasets.builder import ROTATED_DATASETS
from mmdet.datasets.custom import CustomDataset

@ROTATED_DATASETS.register_module()
class MIGHTYDataset(CustomDataset):
    CLASSES = ('slice',)
    PALETTE = [
        (0, 255, 0),
    ]
