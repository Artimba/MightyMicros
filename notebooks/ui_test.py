import sys 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
import cv2

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

        #elf.StopBTN = QPushButton("Stop Recording")
        #self.StopBTN.setEnabled(False)
        #self.layout.addWidget(self.StopBTN)
        #self.StopBTN.clicked.connect(self.ClickStop)


        

    
     

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
            self.Thread2 = Thread2(self) 
            self.Thread2.start() 
        else: 
            self.StartBTN.setText("Start Recording")
            self.Timer.stop() 
            self.ThreadActive = False 
            #self.Thread2.stop()
            self.Thread2.quit() 



       #self.StopBTN.setEnabled(True)

  
      
    
    #def ClickStop(self): 
        #disable button 
        #self.StopBTN.setEnabled(False)
        #self.StartBTN.setEnabled(True)

        
        

#class for a thread to display live camera feed
class Thread1(QThread):
    ImageUpdate = pyqtSignal(QImage) #defining a signal, QImage is a data type 

    def run(self):
        self.ThreadActive = True #boolean 
        Capture = cv2.VideoCapture(0) #get video feed
        while self.ThreadActive: 
            ret, frame = Capture.read() #get frame from video feed
            if ret: 
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #get color image from feed
                #FlippedImage = cv2.flip(Image, 1) #flip video on vertical axis 
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888) #convert to a format that qt can read 
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio) #scale the image 
                self.ImageUpdate.emit(Pic) #emit the thread: send to main window 

    def stop(self): 
        self.ThreadActive = False #stops while loop 
        self.quit()


#class for a thread to write video to a file 
class Thread2(QThread):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ThreadActive = True

    def run(self):

        if self.ThreadActive:
            self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.Output = cv2.VideoWriter('video_recording.mp4', self.Fourcc, 20, (640, 480))
            self.Capture = cv2.VideoCapture(0)

            print("Sanity Check ", self.Capture.isOpened())
            while self.ThreadActive: 
                ret, frame = self.Capture.read() 
                if ret: 
                    self.Output.write(frame)                  

    def stop(self):
        #self.ThreadActive = False
        self.Output.release()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec()) #execute application