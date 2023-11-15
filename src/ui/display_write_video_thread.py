import os
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2

from src.pipeline.detection import Model
from src import PROJECT_ROOT

class Video(object): 
    def __init__(self): 
        self.ThreadActive = True

    def start_feed(self, camera_number: int): 
        Capture = cv2.VideoCapture(0)

        # This is used over just a string for OS interoperability
        weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')

        self.model = Model(weights_path)
        self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.Output = cv2.VideoWriter('video_recording'+str(camera_number)+'.mp4', self.Fourcc, 20, (640, 480))

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret: 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #get color image from feed
                frame = cv2.resize(frame, (640, 480))

                results = self.model.predict(frame)
                
                annotated_frame = results[0].plot(labels=False, masks=False)

                qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                self.ImageUpdate.emit(qt_frame) #emit the thread: send to main window 

                if self.ThreadActive: 
                    self.Output.write(frame)


        def stop_thread(): 
            self.ThreadActive = False 
            self.Output.release()




#class for a thread to display video and write video to a file 
class Thread1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, camera_number: int, parent = None):
        super(Thread1, self).__init__(parent)
        #self.ThreadActive = True 
        self.camera_number = camera_number


    def run(self):
        video = Video()
        video.start_feed(self.camera_number)
        

    def stop(self):
        #video.stop_thread()
        self.quit()
        
