import os
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2

from src.pipeline.detection import Model
from src import PROJECT_ROOT


#class for a thread to display video and write video to a file 
class Thread1(QThread):
    

    def __init__(self, videoNumber: int, isRecord: bool, frame1: QImage, parent = None):
        super(Thread1, self).__init__(parent)
        self.videoNumber = videoNumber
        self.ThreadActive = True 
        self.isRecord = isRecord
        self.frame1 = frame1

    def run(self):
        
        # This is used over just a string for OS interoperability
        #weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')

        #self.model = Model(weights_path)
        self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.Output = cv2.VideoWriter('video_recording_1_'+str(self.videoNumber)+'.mp4', self.Fourcc, 20, (640, 480))

        #self.Capture = cv2.VideoCapture(0)

        while self.ThreadActive: 
                if self.isRecord: 

                    frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_RGB2BGR)
                    self.Output.write(frame1)

    def stop(self):
        self.ThreadActive = False
        self.Output.release()
        self.quit()
        
#class for a thread to display video and write video to a file 
#recording the camera feed that is on the right hand side is not working for some reason 
class Thread2(QThread):

    def __init__(self, videoNumber: int, isRecord: bool, frame2: QImage, parent = None):
        super(Thread2, self).__init__(parent)
        self.videoNumber = videoNumber
        self.ThreadActive = True #- see if commenting this out works
        self.isRecord = isRecord
        self.frame2 = frame2

    def run(self):
        
        # This is used over just a string for OS interoperability
        #weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')

        #self.model = Model(weights_path)
        self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.Output = cv2.VideoWriter('video_recording_2_'+str(self.videoNumber)+'.mp4', self.Fourcc, 15, (640, 480))

        #self.Capture = cv2.VideoCapture(0)

        while self.ThreadActive: 
                if self.isRecord: 
                    frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_RGB2BGR)
                    self.Output.write(frame2)

    def stop(self):
        self.ThreadActive = False
        self.Output.release()
        self.quit()
        
