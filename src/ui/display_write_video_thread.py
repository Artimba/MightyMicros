import os
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2
import numpy as np
from sys import settrace, stdout, stderr

from src import PROJECT_ROOT
from src.pipeline.detection import Model, DetectionManager
# from src.entry import StreamToLogger


import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')


def my_tracer(frame, event, arg = None): 
    # extracts frame code 
    code = frame.f_code 
  
    # extracts calling function name 
    func_name = code.co_name 
  
    # extracts the line number 
    line_no = frame.f_lineno 
  
    print(f"A {event} encountered in {func_name}() at line number {line_no} ") 
  
    return my_tracer





class VideoThread(QThread):
    frame_signal = pyqtSignal(QImage)
    camera_failed_signal = pyqtSignal(int)
    
    def __init__(self, camera_index: int, output1: QTextEdit, output2: QTextEdit, parent=None):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_index)
        self.camera_index = camera_index
        self.model = Model(os.path.join(PROJECT_ROOT, 'pipeline', 'runs/detect/train5/weights/best.pt'), output1, output2)
        self.save_path = os.path.join(PROJECT_ROOT, 'recordings')
        self.thread_active = True
        self.video_writer = None
        self.is_recording = False
        #self.numSlices = 1
       #self.currentSlicesFrame = [0]
        self.output1 = output1
        self.output2 = output2
        self.setObjectName(f"VideoThread_{camera_index}")
        logger.info(f'VideoThread initialized with camera index {self.camera_index}')
    
    def run(self):
        logging.info(f'VideoThread running')
        while self.thread_active:
            success, frame = self.camera.read()
            if success:
                frame = cv2.resize(frame, (640, 480))
                #results = self.model.track(frame)
                if self.camera_index == 1: 
                    annotated_frame, results = self.model.predict(frame)
                else: 
                    annotated_frame = frame
                #annotated_frame = results[0].plot(labels=False, masks=False)

                
                        
                #output slice number detected to console
                # if self.camera_index == 1: 
                #     num_of_slices = len(results[0])
                    

                #     if num_of_slices not in self.currentSlicesFrame: 
                #         slices_to_add = num_of_slices - max(self.currentSlicesFrame)
                    

                #         for i in range(0, slices_to_add):
                #             self.output1.append("Slice " + str(self.numSlices) + " detected" )
                #             self.output2.append("Slice " + str(self.numSlices) + " detected" )
                #             self.numSlices +=1
                            
                            

                        
                #     self.currentSlicesFrame.append(num_of_slices)

             

                if self.is_recording:
                    try:
                        self.video_writer.write(annotated_frame)
                    except Exception as e:
                        logger.info(f'Error writing frame to video file: {e}')
                        self.stop_recording()
                        
                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888)
                qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.frame_signal.emit(qt_frame)
            
            # This was an attempt to fix the camera freezing midway through issue
            if self.camera.isOpened() == False:
                self.camera.release()
                logger.info(f'released camera {self.camera_index}')
                self.camera_failed_signal.emit(self.camera_index)
    
    
    
    def start_recording(self, video_number: int):
        logger.info(f"Camera {self.camera_index} starting recording")
        if not self.is_recording:
            # TODO: Hardcoded 0 for camera number because camera_index is currently a path to a data file for testing. Should be set back to {self.camera_index} when we are using real cameras.
            self.video_writer = cv2.VideoWriter(os.path.join(self.save_path, f'video_recording_{self.camera_index}_{video_number}.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 10, (640, 480))
            logger.info(f"Video Writer Initialized: {self.video_writer}")
            self.is_recording = True
            
    def stop_recording(self):
        logger.info(f"Camera {self.camera_index} stopping recording")
        if self.is_recording:
            logger.info("Video Writer Released")
            self.is_recording = False
            self.video_writer.release()
            self.video_writer = None
    
    def stop(self):
        self.thread_active = False
        self.camera.release()
        try:
            self.video_writer.release()
        except Exception as e:
            pass
        self.quit()
        self.wait()