from mmrotate.datasets.builder import ROTATED_DATASETS
from mmrotate.datasets.dota import DOTADataset

@ROTATED_DATASETS.register_module()
class MIGHTYDataset(DOTADataset):
    CLASSES = ('slice',)
    PALETTE = [
        (0, 255, 0),
    ]