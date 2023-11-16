import os
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2

from src.pipeline.detection import Model
from src import PROJECT_ROOT

#sources: 
#https://www.youtube.com/watch?v=a6_5vkxLwAw&t=1485s
#https://stackoverflow.com/questions/62279279/how-to-record-the-video-from-a-webcam-in-a-pyqt5-gui-using-opencv-and-qthread


#class for a thread to display video and write video to a file 
class Thread1(QThread):
    #ImageUpdate = pyqtSignal(QImage)

    def __init__(self, cameraNumber: int, frame, parent = None):
        super(Thread1, self).__init__(parent)
        self.cameraNumber = cameraNumber
        self.ThreadActive = True
        self.frame = frame

        

    def run(self):
        #Capture = cv2.VideoCapture(0) #get video feed
        
        # This is used over just a string for OS interoperability
        #weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')

        #self.model = Model(weights_path)
        self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.Output = cv2.VideoWriter('video_recording'+str(self.cameraNumber)+'.mp4', self.Fourcc, 20, (640, 480))

        #self.Capture = cv2.VideoCapture(0)

        #while self.ThreadActive: 
            #ret, frame = Capture.read() #get frame from video feed
            #if ret: 
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #get color image from feed
                #frame = cv2.resize(frame, (640, 480))
                
        
                #results = self.model.predict(frame)
                
                #annotated_frame = results[0].plot(labels=False, masks=False)

            
                
                #qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                #qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                
                #qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                #self.ImageUpdate.emit(qt_frame) #emit the thread: send to main window 

        if self.ThreadActive: 
            annotated_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            self.Output.write(self.frame)

    def stop(self):
        self.ThreadActive = False
        self.Output.release()
        self.quit()
        

#display thread: emits threads, opens camera and emits frame 
#pass signal from display thread to record thread 

#open camera in main window that is called update?

#to create two cameras do I need multiple threads for each camera?

#init: qtimer(self) and videocapture open in init, attach timer.timeout.connect(self.updateFrame) - method I haven't made yet 
    #self.timer.start(30)
#updateFrame function: ret, camera self.camrea.read (similar to thread1)
    #update pixmap
#comment out thread1

#open writer in init 