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
from src.pipeline.model import Model
# from src.entry import StreamToLogger


import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')


REC_FPS = 30 # FPS for recording videos

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
    console_signal = pyqtSignal(str)
    
    def __init__(self, camera_index: int, save_path: str, do_detections=True, parent=None):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_index[1])
        self.camera_index = camera_index[0]
        self.model = Model()
        self.save_path = save_path
        self.thread_active = True
        self.video_writer = None
        self.is_recording = False
        self.do_detections = do_detections
        self.valid_ids = []
        self.setObjectName(f"VideoThread_{camera_index}")
        logger.info(f'VideoThread initialized with camera index {self.camera_index}')
    
    def run(self):
        logging.info(f'VideoThread running')
        while self.thread_active:

            
            success, frame = self.camera.read()
            if success:
                frame = cv2.resize(frame, (640, 480))
                if self.do_detections:
                    annotated_frame = self.model.predict(frame)
                    for detection in self.model.manager.detections.values(): 
                        if detection.id not in self.valid_ids and self.camera_index == 1: # TODO: Remove for prod
                            self.console_signal.emit(f"Slice Found: {detection.id}")
                            self.valid_ids.append(detection.id)
                else:
                    annotated_frame = frame
                
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
            self.video_writer = cv2.VideoWriter(os.path.join(self.save_path, f'video_recording_{self.camera_index}_{video_number}.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), REC_FPS, (640, 480))
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