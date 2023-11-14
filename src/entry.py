from PyQt5.QtWidgets import QApplication
from sys import argv, __excepthook__, excepthook, exit

from src.ui.head import MightyMicros

def run():
    app = QApplication(argv)
    gui = MightyMicros()
    gui.show()
    exit(app.exec_())

if __name__ == '__main__':
    run()