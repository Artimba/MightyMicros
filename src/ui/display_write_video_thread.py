import os
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2
import numpy as np
from sys import settrace, stdout, stderr
import queue

from src import PROJECT_ROOT
from src.pipeline.detection import Model
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

class CameraThread(QThread):
    raw_frame_signal = pyqtSignal(np.ndarray)
    
    def __init__(self, camera_index: int, parent=None):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_index)
        self.camera_index = camera_index
        self.thread_active = True
        self.setObjectName(f"CameraThread_{camera_index}")
        logger.info(f'CameraThread initialized with camera index {self.camera_index}')
        
    def run(self):
        logging.info(f'CameraThread running')
        while self.thread_active:
            success, frame = self.camera.read()
            if success:
                frame = cv2.resize(frame, (640, 480))
                self.raw_frame_signal.emit(frame)
    
    def stop(self):
        self.thread_active = False
        self.camera.release()
        self.quit()
        self.wait()

class ProcessingThread(QThread):
    annotated_frame_signal = pyqtSignal(QImage)
    frame_for_recording_signal = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = Model(os.path.join(PROJECT_ROOT, 'pipeline', 'runs/detect/train4/weights/best.pt'))
        self.frame_queue = queue.Queue()
        self.thread_active = True
        self.setObjectName("ProcessingThread")
        logger.info('ProcessingThread initialized')

    def run(self):
        logging.info(f'ProcessingThread running')
        while self.thread_active:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                annotated_frame = self.model.predict(frame)[0].plot(labels=False, masks=False)
                self.frame_for_recording_signal.emit(annotated_frame)
                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                qt_frame = QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888)
                qt_frame = qt_frame.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.annotated_frame_signal.emit(qt_frame)

    @pyqtSlot(np.ndarray)
    def process_frame(self, frame: np.ndarray):
        self.frame_queue.put(frame)

    def stop(self):
        self.thread_active = False
        self.quit()
        self.wait()

class RecordingThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RecordingThread")
        self.frame_queue = queue.Queue()
        self.video_writer = None
        self.is_recording = False
        self.thread_active = True
        logger.info('RecordingThread initialized')

    def run(self):
        logging.info(f'RecordingThread running')
        while self.thread_active:
            logger.info(len(self.frame_queue.queue))
            if not self.frame_queue.empty() and self.is_recording and self.video_writer is not None:
                logger.info("LAG?")
                frame = self.frame_queue.get()           
                self.video_writer.write(frame)


    @pyqtSlot(np.ndarray)
    def record_frame(self, frame: np.ndarray):
        if self.is_recording:
            self.frame_queue.put(frame)

    def start_recording(self, camera_idx: int, video_number: int):
        logger.info("RecordingThread starting recording")
        if not self.is_recording:
            self.is_recording = True
            self.video_writer = cv2.VideoWriter(f'video_recording_{camera_idx}_{video_number}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
            
    def stop_recording(self):
        logger.info("RecordingThread stopping recording")
        if self.is_recording:
            self.is_recording = False
            self.video_writer.release()
            self.video_writer = None

    def stop(self):
        self.thread_active = False
        try:
            self.video_writer.release()
        except AttributeError:
            pass
        self.quit()
        self.wait()
