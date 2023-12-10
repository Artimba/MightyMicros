from PyQt5.QtWidgets import QApplication
from sys import argv, __excepthook__, excepthook, exit

import logging
from src.ui.head import MightyMicros


def run():
    logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('Detection_Model')
    logger.info('Starting Detection_Model')
    app = QApplication(argv)
    gui = MightyMicros()
    gui.show()
    exit(app.exec_())

if __name__ == '__main__':
    run()