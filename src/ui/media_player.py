#sources:
#https://www.youtube.com/watch?v=a6_5vkxLwAw&t=1485s

#import libraries
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
        self.setGeometry(350, 100, 700, 500)

       
        self.init_ui()

        self.show()

    def init_ui(self): 

        #create media player
        self.MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create video widget 
        self.VideoWidget = QVideoWidget()

        #create open button 
        self.OpenBTN = QPushButton('Open Video')
        self.OpenBTN.clicked.connect(self.openFile)

        #create play button 
        self.StartBTN = QPushButton("Play") 
        self.StartBTN.setEnabled(False)
        self.StartBTN.clicked.connect(self.playVideo)

        #create slider 
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setRange(0,1)
        #self.Slider.setEnabled(False)
        self.Slider.sliderMoved.connect(self.setPosition)
        

        #create label 
        self.Label = QLabel()
        self.Label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create layouts
        HboxLayout = QHBoxLayout()
        HboxLayout.setContentsMargins(0, 0, 0, 0)
        VboxLayout = QVBoxLayout()

        #add widgets to the hbox layout 
        HboxLayout.addWidget(self.OpenBTN)
        HboxLayout.addWidget(self.StartBTN)
        HboxLayout.addWidget(self.Slider)


        #add widgets to the vbox layout 
        VboxLayout = QVBoxLayout()
        VboxLayout.addWidget(self.VideoWidget)
        VboxLayout.addLayout(HboxLayout)
        VboxLayout.addWidget(self.Label)

        #add layouts 
        self.setLayout(VboxLayout)
        self.setLayout(HboxLayout)

        self.MediaPlayer.setVideoOutput(self.VideoWidget)
        self.MediaPlayer.stateChanged.connect(self.mediaStateChange)
        self.MediaPlayer.positionChanged.connect(self.positionChanged)
        self.MediaPlayer.durationChanged.connect(self.durationChanged)

    #function to open a video file
    def openFile(self): 
        filename, _= QFileDialog.getOpenFileName(self, "Open Video")

        if filename != "": 
            self.MediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.StartBTN.setEnabled(True)



    #function to pause and play video
    def playVideo(self): 
        if self.MediaPlayer.state() == QMediaPlayer.PlayingState: 
            self.MediaPlayer.pause()
            
        else: 
            self.MediaPlayer.play()

    #function to change button icon 
    def mediaStateChange(self, state): 
        if self.MediaPlayer.state() == QMediaPlayer.PlayingState: 
            self.StartBTN.setText("Pause")

        else: 
            
            self.StartBTN.setText("Play")
            

    #functions to change the position and duration of the slider
    def positionChanged(self, position): 
        self.Slider.setValue(position)

    def durationChanged(self, duration): 
        self.Slider.setRange(0, duration)

    def setPosition(self, position): 
        self.MediaPlayer.setPosition(position)

    #function to handle errors
    def handleError(self): 
        self.StartBTN.setEnabled(False)
        self.Label.setText("Error: " + self.mediaPlayer.errorString())




if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec()) #execute application
