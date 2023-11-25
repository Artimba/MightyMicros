import os
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2
import numpy as np
from sys import settrace


from src import PROJECT_ROOT
from src.pipeline.detection import Model





def my_tracer(frame, event, arg = None): 
    # extracts frame code 
    code = frame.f_code 
  
    # extracts calling function name 
    func_name = code.co_name 
  
    # extracts the line number 
    line_no = frame.f_lineno 
  
    print(f"A {event} encountered in {func_name}() at line number {line_no} ") 
  
    return my_tracer

#settrace(my_tracer)

#class for a thread to display video and write video to a file 
class Thread1(QThread):
    

    def __init__(self, videoNumber: int, frame: np.ndarray, output: cv2.VideoWriter, parent = None):
        super(Thread1, self).__init__(parent)
        self.videoNumber = videoNumber
        self.ThreadActive = True 
        self.Output = output
        
        self.frame = frame

    def run(self):
        
        # This is used over just a string for OS interoperability
        
        

        while self.ThreadActive: 
            frame1 = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            self.Output.write(frame1)
       

    def stop(self):
        self.ThreadActive = False
        #self.Output.release()
        self.quit()
        
#class for a thread to display video and write video to a file 
#recording the camera feed that is on the right hand side is not working for some reason 
class Thread2(QThread):

    def __init__(self, videoNumber: int, frame: np.ndarray, output: cv2.VideoWriter, parent = None):
        super(Thread2, self).__init__(parent)
        self.videoNumber = videoNumber
        self.ThreadActive = True #- see if commenting this out works
        self.Output = output
        self.frame = frame

    def run(self):
        
        # This is used over just a string for OS interoperability
    
        

        while self.ThreadActive: 

                   
            frame2 = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            self.Output.write(frame2)
    


    def stop(self):
        self.ThreadActive = False
        #self.Output.release()
        self.quit()


#thread class to run model on frames
class Thread3(QThread):
    frame_edit = pyqtSignal(QImage)

    def __init__(self, frame: np.ndarray, parent = None):
        super(Thread3, self).__init__(parent)
        self.frame = frame
        self.weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')
        self.model = Model(self.weights_path)
        

    def run(self):
        
        results = self.model.predict(self.frame)
        annotated_frame = results[0].plot(labels=False, masks=False)
        qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888)
        qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
        
        self.frame_edit.emit(qt_frame)

    def stop(self):
        self.quit()


        
