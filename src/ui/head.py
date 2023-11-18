import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os

from src.ui.main_ui import Ui_MainWindow
from src.ui.display_write_video_thread import Thread1, Thread2

#sources: 
#https://www.youtube.com/watch?v=a6_5vkxLwAw&t=1485s
#https://stackoverflow.com/questions/62279279/how-to-record-the-video-from-a-webcam-in-a-pyqt5-gui-using-opencv-and-qthread




class MightyMicros(QtWidgets.QMainWindow):

    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

        # Change/add any property about ui here
        self.videoNumber = 1
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.frame_5.setMinimumSize(QtCore.QSize(440, 330))

        # region [ Widgets ]

        # region [Add combo box widget] 
        self.videoCombo = QtWidgets.QComboBox(self.ui.frame_4)
        self.ui.horizontalLayout_12.addWidget(self.videoCombo)

        # endregion
        # region [ Add widgets]
        self.mediaPlayer1 = QMediaPlayer(self.ui.frame_5, QMediaPlayer.VideoSurface)
        self.videoWidget1 = QVideoWidget()
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        self.mediaPlayer1.setObjectName("media_player1")
        self.ui.horizontalLayout_13.insertWidget(0, self.videoWidget1)

        self.mediaPlayer2 = QMediaPlayer(self.ui.frame_5, QMediaPlayer.VideoSurface)
        self.videoWidget2 = QVideoWidget() 
        self.mediaPlayer2.setObjectName("media_player2")
        self.ui.horizontalLayout_13.insertWidget(1, self.videoWidget2)

        self.output1 = QtWidgets.QTextEdit(self.ui.ConFrame)
        self.output1.setObjectName("output1")
        self.ui.verticalLayout_4.addWidget(self.output1)
        self.output2 = QtWidgets.QTextEdit(self.ui.ConFrame_2)
        self.output2.setObjectName("output2")
        self.ui.verticalLayout_7.addWidget(self.output2)

        # endregion

        # region [ Delete widgets ]

        self.ui.horizontalLayout_13.removeWidget(self.ui.label_9)
        self.ui.label_9.deleteLater()
        self.ui.label_9 = None

        self.ui.verticalLayout_4.removeWidget(self.ui.graphicsView)
        self.ui.graphicsView.deleteLater()
        self.ui.graphicsView = None 

        self.ui.verticalLayout_7.removeWidget(self.ui.graphicsView_2)
        self.ui.graphicsView_2.deleteLater()
        self.ui.graphicsView_2 = None

        #self.ui.horizontalLayout_15.removeWidget(self.ui.label_7)
        #self.ui.label_7.deleteLater() 
        #self.ui.label_7 = None

        #self.ui.horizontalLayout_15.removeWidget(self.ui.label_8)
        #self.ui.label_8.deleteLater() 
        #self.ui.label_8 = None


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
        self.output1.setReadOnly(True)
        self.output2.setReadOnly(True)

        # endregion
        # endregion
        
        self.ui.tabWidget.setCurrentIndex(0)
        
        # region [ Signals ]
        self.timer = QtCore.QTimer()

        
        self.ui.pushButton.clicked.connect(self.ClickBTN)
        
        self.Thread1 = Thread1(self.videoNumber, False)
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot1)
        
        self.Thread2 = Thread2(self.videoNumber, False)
        self.Thread2.start()
        self.Thread2.ImageUpdate.connect(self.ImageUpdateSlot2)

        self.ui.pushButton_2.clicked.connect(self.playVideo1)
        
        self.mediaPlayer1.setVideoOutput(self.videoWidget1)
        self.mediaPlayer2.setVideoOutput(self.videoWidget2)

        self.mediaPlayer1.stateChanged.connect(self.mediaStateChange1)
        self.mediaPlayer1.positionChanged.connect(self.positionChanged1)
        self.mediaPlayer1.durationChanged.connect(self.durationChanged1)

        self.ui.pushButton_5.clicked.connect(self.playVideo2)
        
    
        self.mediaPlayer2.stateChanged.connect(self.mediaStateChange2)
        self.mediaPlayer2.positionChanged.connect(self.positionChanged2)
        self.mediaPlayer2.durationChanged.connect(self.durationChanged2)

        self.videoCombo.currentTextChanged.connect(self.comboBoxChanged)
        # endregion
        
        # region [ Translation ]
        _translate = QtCore.QCoreApplication.translate
        self.ui.pushButton_2.setText(_translate("MainWindow", "Play"))
        self.ui.pushButton_5.setText(_translate("MainWindow", "Play"))
        self.ui.label_3.setText(_translate("MainWindow", ""))
        self.ui.label_4.setText(_translate("MainWindow", ""))
        # endregion
        
     
   
    # region [ Methods ]
    def ImageUpdateSlot1(self, Image): 
        self.ui.label_3.setPixmap(QtGui.QPixmap.fromImage(Image)) 

    def ImageUpdateSlot2(self, Image): 
        self.ui.label_4.setPixmap(QtGui.QPixmap.fromImage(Image)) 

    def ClickBTN(self):
        #disable start button so user can't click it
        if self.timer.isActive() == False:
            self.ui.pushButton.setText("Stop Recording")  
            self.timer.start() #start the timer

            #start writing the video
            self.ThreadActive = True
            self.Thread1 = Thread1(self.videoNumber, True, self)
            self.Thread1.start()

            self.Thread2 = Thread2(self.videoNumber, True, self)
            self.Thread2.start() 

            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Started")
            
        else: 
            self.ui.pushButton.setText("Start Recording")
            self.timer.stop() 
            self.Thread1.stop()
            self.Thread2.stop()

            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Stopped")
            self.videoCombo.addItem('Video ' + str(self.videoNumber))
            self.videoNumber += 1

            #load video to media player
            
            # TODO: Hard-coded paths are bad for maintainability. Use relative path instead (see what I did inside display_write_video_thread), or prompt for file path. See https://stackoverflow.com/questions/7165749/open-file-dialog-in-pyqt
            #filename = 'video_recording.mp4'
            #self.mediaPlayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(filename)))
            #self.ui.pushButton_2.setEnabled(True)

    #function to change button text 
    def mediaStateChange1(self, state): 
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState: 
            self.ui.pushButton_2.setText("Pause")
        else: 
            self.ui.pushButton_2.setText("Play")

    #functions to change the position and duration of the slider
    def positionChanged1(self, position):
        self.slider_1.setValue(position)

    def durationChanged1(self, duration): 
        self.slider_1.setRange(0, duration)

    def setPosition1(self, position): 
        self.mediaPlayer1.setPosition(position)

    def playVideo1(self): 
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState: 
            self.mediaPlayer1.pause()
        else: 
            self.mediaPlayer1.play()

    #function to change button text 
    def mediaStateChange2(self, state): 
        if self.mediaPlayer2.state() == QMediaPlayer.PlayingState: 
            self.ui.pushButton_5.setText("Pause")
        else: 
            self.ui.pushButton_5.setText("Play")

    #functions to change the position and duration of the slider
    def positionChanged2(self, position):
        self.slider_2.setValue(position)

    def durationChanged2(self, duration): 
        self.slider_2.setRange(0, duration)

    def setPosition2(self, position): 
        self.mediaPlayer2.setPosition(position)

    def playVideo2(self): 
        if self.mediaPlayer2.state() == QMediaPlayer.PlayingState: 
            self.mediaPlayer2.pause()
        else: 
            self.mediaPlayer2.play()
    
    #function to load both videos into media player when the combo box value is changed 
    def comboBoxChanged(self, value): 
        QtTest.QTest.qWait(1000)

        cb_value = str(value)
        num = ''
        for i in cb_value: 
            if i.isdigit():
                num += i

        self.mediaPlayer1.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(os.getcwd()+'/video_recording_1_'+num+'.mp4')))
        self.mediaPlayer2.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(os.getcwd()+'/video_recording_2_'+num+'.mp4')))

        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)

    
    def closeEvent(self, event: QtGui.QCloseEvent):
        """This method handles any cleanup when the application is about to quit.
        
        i.e closing files, releasing threads. 
        """
        
        if self.Thread1.isRunning():
            print("Stopping VideoCapture Thread")
            self.Thread1.stop()
            self.Thread1.wait()

        if self.Thread2.isRunning(): 
            print("Stopping VideoCapture Thread")
            self.Thread2.stop()
            self.Thread2.wait()
        
        print("Closing application")
        # Pass the event back to the normal handler to close the window.
        super().closeEvent(event)
        
    # endregion
          