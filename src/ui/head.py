import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys

from src.ui.main_ui import Ui_MainWindow
from src.ui.display_write_video_thread import Thread1

class MightyMicros(object):
    def __init__(self):
            self.app = QtWidgets.QApplication(sys.argv)
            self.MainWindow = QtWidgets.QMainWindow()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self.MainWindow)

            # Change/add any property about ui here
            
            # region [ Widgets ]
            # region [ Add video widget]
            self.mediaPlayer = QMediaPlayer(self.ui.frame_5, QMediaPlayer.VideoSurface)
            self.videoWidget = QVideoWidget()
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            self.mediaPlayer.setObjectName("media_player")
            self.ui.horizontalLayout_13.insertWidget(0, self.videoWidget)
            # endregion
            
            # region [ Add slider 1 ]
            self.slider_1 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.ui.frame_6)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.slider_1.sizePolicy().hasHeightForWidth())
            self.slider_1.setSizePolicy(sizePolicy)
            self.slider_1.setMinimumSize(QtCore.QSize(440, 0))
            self.slider_1.setObjectName("slider1")
            self.ui.horizontalLayout_14.insertWidget(0, self.slider_1)
            # endregion

            # region [ Add slider 2]
            self.slider_2 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.ui.frame_6)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.slider_2.sizePolicy().hasHeightForWidth())
            self.slider_2.setSizePolicy(sizePolicy)
            self.slider_2.setMinimumSize(QtCore.QSize(440, 0))
            self.slider_2.setObjectName("slider2")
            self.ui.horizontalLayout_14.insertWidget(2, self.slider_2)
            # endregion
            # endregion
            
            self.ui.tabWidget.setCurrentIndex(0)
            
            # region [ Signals ]
            self.timer = QtCore.QTimer()
            self.ui.pushButton.clicked.connect(self.ClickBTN)
            
            self.Thread1 = Thread1()
            self.Thread1.start()
            self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)
            
            self.ui.pushButton_2.clicked.connect(self.playVideo)
            
            self.mediaPlayer.setVideoOutput(self.videoWidget)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChange)
            self.mediaPlayer.positionChanged.connect(self.positionChanged)
            self.mediaPlayer.durationChanged.connect(self.durationChanged)
            # endregion
            
            # region [ Translation ]
            _translate = QtCore.QCoreApplication.translate
            self.ui.pushButton_2.setText(_translate("MainWindow", "Play"))
            self.ui.pushButton_5.setText(_translate("MainWindow", "Play"))
            # endregion
    
    # region [ Signalscope ]
    def ImageUpdateSlot(self, Image): 
        self.ui.label_3.setPixmap(QtGui.QPixmap.fromImage(Image)) 

    def ClickBTN(self):
        #disable start button so user can't click it
        if self.timer.isActive() == False:
            self.ui.pushButton.setText("Stop Recording")  
            self.timer.start() #start the timer
            #start writing the video
            self.ThreadActive = True 
            self.Thread1 = Thread1(self) 
            self.Thread1.start() 
        else: 
            self.pushButton.setText("Start Recording")
            self.timer.stop() 
            self.Thread1.stop()

            #load video to media player
            QtTest.QTest.qWait(1000)
            filename = '/Users/adarekar/Desktop/MightyMicros/video_recording.mp4'
            self.mediaPlayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(filename)))
            self.ui.pushButton_2.setEnabled(True)

    #function to change button icon 
    def mediaStateChange(self, state): 
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState: 
            self.ui.pushButton_2.setText("Pause")
        else: 
            self.ui.pushButton_2.setText("Play")

    #functions to change the position and duration of the slider
    def positionChanged(self, position):
        self.slider_1.setValue(position)

    def durationChanged(self, duration): 
        self.slider_1.setRange(0, duration)

    def setPosition(self, position): 
        self.mediaPlayer.setPosition(position)

    def playVideo(self): 
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState: 
            self.mediaPlayer.pause()
        else: 
            self.mediaPlayer.play()
    # endregion
        
    def run(self):
          self.MainWindow.show()
          sys.exit(self.app.exec_())
          