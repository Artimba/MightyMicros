#sources: 
#https://www.youtube.com/watch?v=a6_5vkxLwAw&t=1485s
#https://stackoverflow.com/questions/62279279/how-to-record-the-video-from-a-webcam-in-a-pyqt5-gui-using-opencv-and-qthread

#import libraries
import sys 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2
from display_write_video_thread import Thread1

#main window object
class MainWindow(QWidget): #main window inherits from QWidget class 
    def __init__(self): 
        super(MainWindow, self).__init__()


        #create layout for QWidget
        self.layout = QVBoxLayout()

        #create widgets
        self.FeedLabel = QLabel() #label will show camera feed
        self.layout.addWidget(self.FeedLabel) #add widget to layout

        self.StartBTN = QPushButton("Start Recording")
        self.Timer = QTimer()
        self.layout.addWidget(self.StartBTN)
        self.StartBTN.clicked.connect(self.ClickBTN)

        self.Thread1 = Thread1() #create instance of thread class
        self.Thread1.start() #start thread 
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot) #connect thread

        #set layout
        self.setLayout(self.layout)

    #connect emitted signal to slot 
    def ImageUpdateSlot(self, Image): 
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image)) 

    #function for when record button is clicked 
    def ClickBTN(self):
        #disable start button so user can't click it
        

        if self.Timer.isActive() == False:
            self.StartBTN.setText("Stop Recording")  
            self.Timer.start() #start the timer
            #start writing the video
            self.ThreadActive = True 
            self.Thread1 = Thread1(self) 
            self.Thread1.start() 
        else: 
            self.StartBTN.setText("Start Recording")
            self.Timer.stop() 
            self.Thread1.stop()


                                    


        


if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec()) #execute application
