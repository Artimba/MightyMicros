import PyQt5.QtWidgets as QtWidgets
from src.ui.main_ui_v2 import Ui_MainWindow
import sys

class MightyMicros(object):
    def __init__(self):
            self.app = QtWidgets.QApplication(sys.argv)
            self.MainWindow = QtWidgets.QMainWindow()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self.MainWindow)

            # Change any property about ui here
        
    def run(self):
          self.MainWindow.show()
          sys.exit(self.app.exec_())
            