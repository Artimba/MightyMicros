import sys 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2

#class for a thread to display video and write video to a file 
class Thread1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ThreadActive = True #- see if commenting this out works

    def run(self):
        Capture = cv2.VideoCapture(0) #get video feed

     
        self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.Output = cv2.VideoWriter('video_recording.mp4', self.Fourcc, 20, (640, 480))
        #self.Capture = cv2.VideoCapture(0)

        while True: 
            ret, frame = Capture.read() #get frame from video feed
            if ret: 
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #get color image from feed
                frame = cv2.resize(frame, (640, 480))
                #FlippedImage = cv2.flip(Image, 1) #flip video on vertical axis 
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                self.ImageUpdate.emit(Pic) #emit the thread: send to main window 

                if self.ThreadActive: 
                    self.Output.write(frame)

    def stop(self):
        self.ThreadActive = False
        self.Output.release()
        self.quit()