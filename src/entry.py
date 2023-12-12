from PyQt5.QtWidgets import QApplication
from sys import argv, __excepthook__, excepthook, exit

import logging
from src.ui.head import MightyMicros
from src.download_model import download_from_drive


def run():
    logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('YOLO_Detection')
    download_from_drive()
    logger.info('Starting YOLO_Detection')
    app = QApplication(argv)
    gui = MightyMicros()
    gui.show()
    exit(app.exec_())

if __name__ == '__main__':
    run()