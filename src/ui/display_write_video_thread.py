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



        
class VideoThread(QThread):
    frameSignal = pyqtSignal(QImage)
    def __init__(self, camNum: int):
        super().__init__()
        self.camNum = camNum
        self.weightsPath = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')
        self.model = Model(self.weightsPath)
       
        self.threadActive = True

    def run(self):
        camera = cv2.VideoCapture(self.camNum) 
        
        

        while self.threadActive:  
            ret, frame = camera.read() #get frame from video feed
            if ret:

                if self.camNum == 1: 

                    frame = cv2.resize(frame, (640, 480))
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.model.predict(frame)
                    annotated_frame = results[0].plot(labels=False, masks=False)

                    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB) #get color image from feed

                
                    qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                    #qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 

                    qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                    self.frameSignal.emit(qt_frame)

                elif self.camNum == 0: 
                    frame = cv2.resize(frame, (640, 480))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                    qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 

                    qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                    self.frameSignal.emit(qt_frame)



                
        camera.release()

    def stop(self):
        self.threadActive = False
        self.wait()    
                    

                

                

                #try: 

                    #for i, bbox in enumerate(results[0].boxes.xyxy):
                        #coord = results[0].boxes.xyxy[i].numpy()
                        #self.output1.append("Slice " + str(self.numSlices) + " detected" )
                        #self.numSlices += 1
                        #print(results[0].boxes.xyxy[i])
                        #print(str(results[0].boxes.xyxy[i][0]))
                    
                #except IndexError: 
                    #pass

              

                    


            
                    

                    
                #qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                #qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QtGui.QImage.Format.Format_RGB888) #convert to a format that qt can read 
                
                #qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 

        

class VideoThread2(QThread):
    frameSignal = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.weightsPath = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')
        self.model = Model(self.weightsPath)
       
        self.threadActive = True

    def run(self):
        camera = cv2.VideoCapture(1) 
        
        

        while self.threadActive:  
            ret, frame = camera.read() #get frame from video feed
            if ret:

                

                frame = cv2.resize(frame, (640, 480))
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.model.predict(frame)
                annotated_frame = results[0].plot(labels=False, masks=False)

                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB) #get color image from feed

            
                qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
               #qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 

                qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                self.frameSignal.emit(qt_frame)


                
        camera.release()

    def stop(self):
        self.threadActive = False
        self.wait()


class VideoThread1(QThread):
    frameSignal = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.weightsPath = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')
        self.model = Model(self.weightsPath)
       
        self.threadActive = True

    def run(self):
        camera = cv2.VideoCapture(0) 
        
        

        while self.threadActive:  
            ret, frame = camera.read() #get frame from video feed
            if ret:

                

                frame = cv2.resize(frame, (640, 480))
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.model.predict(frame)
                annotated_frame = results[0].plot(labels=False, masks=False)

                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB) #get color image from feed

            
                qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                #qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 

                qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                self.frameSignal.emit(qt_frame)


                
        camera.release()

    def stop(self):
        self.threadActive = False
        self.wait()
