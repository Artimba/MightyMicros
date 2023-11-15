import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys

from src.ui.main_ui import Ui_MainWindow
from src.ui.display_write_video_thread import Thread1

#sources: 
#https://www.youtube.com/watch?v=a6_5vkxLwAw&t=1485s
#https://stackoverflow.com/questions/62279279/how-to-record-the-video-from-a-webcam-in-a-pyqt5-gui-using-opencv-and-qthread




class MightyMicros(QtWidgets.QMainWindow):

    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

        # Change/add any property about ui here
        self.cameraNumber = 1
        
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

        # region [ Edit TextEdit Widget]
        self.ui.output1.setReadOnly(True)
        self.ui.output2.setReadOnly(True)

        # endregion
        # endregion
        
        self.ui.tabWidget.setCurrentIndex(0)
        
        # region [ Signals ]
        self.timer = QtCore.QTimer()

        
        self.ui.pushButton.clicked.connect(self.ClickBTN)
        
        self.Thread1 = Thread1(self.cameraNumber)
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
        
        # region [ Add Widgets ]

        # endregion
   
    # region [ Methods ]
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
            #output1_text = output1_text + "\nRecording Started"
            self.ui.output1.append("\nRecording Started")
        else: 
            self.ui.pushButton.setText("Start Recording")
            self.timer.stop() 
            self.Thread1.stop()
            #output1_text = output1_text + "\nRecording Stopped"
            self.ui.output1.append("\nRecording Stopped")

            #load video to media player
            QtTest.QTest.qWait(1000)
            # TODO: Hard-coded paths are bad for maintainability. Use relative path instead (see what I did inside display_write_video_thread), or prompt for file path. See https://stackoverflow.com/questions/7165749/open-file-dialog-in-pyqt
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
    
    def closeEvent(self, event: QtGui.QCloseEvent):
        """This method handles any cleanup when the application is about to quit.
        
        i.e closing files, releasing threads. 
        """
        
        if self.Thread1.isRunning():
            print("Stopping VideoCapture Thread")
            self.Thread1.stop()
            self.Thread1.wait()
        
        print("Closing application")
        # Pass the event back to the normal handler to close the window.
        super().closeEvent(event)
        
    # endregion
          