import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtGui import QImage, QPixmap
import PyQt6.QtCore as QtCore

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # capture from camera 1 for instance
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # Convert it to QImage
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                self.changePixmap.emit(p)

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Create two labels
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        # Set up thread and signal for first camera
        self.thread1 = Thread()
        self.thread1.changePixmap.connect(self.setImage1)
        self.thread1.start()

    def setImage1(self, image):
        self.label1.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoWindow()
    window.show()
    sys.exit(app.exec())
