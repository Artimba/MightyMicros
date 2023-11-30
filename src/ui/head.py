import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os
import cv2


from src.ui.main_ui import Ui_MainWindow
from src.ui.display_write_video_thread import CameraThread, ProcessingThread
from src import PROJECT_ROOT
from src.pipeline.detection import Model

import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('YOLO_Detection')


#sources: 
#https://www.youtube.com/watch?v=a6_5vkxLwAw&t=1485s
#https://stackoverflow.com/questions/62279279/how-to-record-the-video-from-a-webcam-in-a-pyqt5-gui-using-opencv-and-qthread




class MightyMicros(QtWidgets.QMainWindow):

    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.video_threads = []
        self.camera_index = 0
        self.temp_data = [0, 1]

        # Change/add any property about ui here
        self.videoNumber = 1
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.frame_5.setMinimumSize(QtCore.QSize(440, 330))
        self.numSlices = 1
        self.isRecord = False
        
        # region [ Widgets ]

        # region [ Set up camera display ]
        #self.camera1 = cv2.VideoCapture(1)
        #self.timer1 = QtCore.QTimer(self)
        #self.timer1.timeout.connect(self.updateFrame1)
        #self.timer1.start(30)

        #self.camera2 = cv2.VideoCapture(0)
        #self.timer2 = QtCore.QTimer(self)
        #self.timer2.timeout.connect(self.updateFrame2)
        #self.timer2.start(30)
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

        self.videoCombo = QtWidgets.QComboBox(self.ui.frame_4)
        self.ui.horizontalLayout_12.addWidget(self.videoCombo)
        
        self.gridBtn = QtWidgets.QPushButton(self.ui.frame_4)
        self.ui.horizontalLayout_12.addWidget(self.gridBtn)

        self.threadBtn1 = QtWidgets.QPushButton(self.ui.CamLabFrame)
        self.ui.horizontalLayout_7.addWidget(self.threadBtn1)

        self.threadBtn2 = QtWidgets.QPushButton(self.ui.CamLabFrame)
        self.ui.horizontalLayout_7.addWidget(self.threadBtn2)

       

        self.popUp = PopUpWindow(self.output2, self)


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
        self.gridBtn.clicked.connect(self.gridPopUp)
        
        #self.Thread1 = Thread1(self.videoNumber, False)
        #self.Thread1.start()
        #self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot1)
        
        #self.Thread2 = Thread2(self.videoNumber, False)
        #self.Thread2.start()
        #self.Thread2.ImageUpdate.connect(self.ImageUpdateSlot2)

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

        self.threadBtn1.clicked.connect(self.InitializeCamera)
        self.threadBtn2.clicked.connect(self.InitializeCamera)
        # endregion
        
        # region [ Translation ]
        _translate = QtCore.QCoreApplication.translate
        self.ui.pushButton_2.setText(_translate("MainWindow", "Play"))
        self.ui.pushButton_5.setText(_translate("MainWindow", "Play"))
        self.ui.label_3.setText(_translate("MainWindow", ""))
        self.ui.label_4.setText(_translate("MainWindow", ""))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.RecordTab), _translate("MainWindow", "Camera Feeds"))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_2), _translate("MainWindow", "Media Players"))
        self.gridBtn.setText(_translate("MainWindow", "Grid Management"))
        self.threadBtn1.setText(_translate("MainWindow", "Show Mighty Micros Camera"))
        self.threadBtn2.setText(_translate("MainWindow", "Show Microtome Camera"))

        # endregion
        
     
   
    # region [ Methods ]
    # def startVideoThreads(self):
    #     # Manage unique integers for threads
    #     indices = [0, 1]

    #     for index in indices: 
    #         videoThread1 = VideoThread(index)

    #         if index == 0: 

    #             videoThread1.frameSignal.connect(self.ImageUpdateSlot1)
    #             videoThread1.start()
    #             self.videoThreads.append(videoThread1)

    #         elif index == 1: 
    #             videoThread1.frameSignal.connect(self.ImageUpdateSlot2)
    #             videoThread1.start()
    #             self.videoThreads.append(videoThread1)

    def InitializeCamera(self):
        # Manage unique integers for threads
        
        if self.camera_index == 0:
            self.ui.label_3.setText("Loading...")
        elif self.camera_index == 1:
            self.ui.label_4.setText("Loading...")
        
        
        logger.info(f"Initializing Camera {self.camera_index}")
        camera_thread = CameraThread(self.temp_data[self.camera_index])
        
        processing_thread = ProcessingThread()
        
        camera_thread.raw_frame_signal.connect(processing_thread.process_frame)
        camera_thread.camera_stopped_signal.connect(processing_thread.stop)
        camera_thread.camera_stopped_signal.connect(camera_thread.stop)
        processing_thread.annotated_frame_signal.connect(lambda image, idx=self.camera_index: self.UpdatePixmap(image, idx))
        
        camera_thread.start()
        processing_thread.start()
                
        self.camera_index += 1
        self.video_threads.append((camera_thread, processing_thread))
    
    def UpdatePixmap(self, Image: QtGui.QImage, camera_index: int):
        if isinstance(camera_index, int) == False:
            logger.info(f"UpdatePixmap called with invalid camera_thread argument, camera_thread is type: {type(camera_index)}. Expected type: int")
        
        if camera_index == 0:
            self.ui.label_3.setPixmap(QtGui.QPixmap.fromImage(Image))
        elif camera_index == 1:
            self.ui.label_4.setPixmap(QtGui.QPixmap.fromImage(Image))

    def ClickBTN(self):
        if self.isRecord == False:
            self.ui.pushButton.setText("Stop Recording")  
            self.timer.start() #start the timer
            for idx, (_, processing_thread) in enumerate(self.video_threads, start=1):
                processing_thread.start_recording(idx, self.videoNumber)
            self.isRecord = True
            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Started")
        else:
            self.ui.pushButton.setText("Start Recording")
            self.timer.stop()
            [processing_thread.stop_recording() for _, processing_thread in self.video_threads]
            self.isRecord = False
            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Stopped")
            self.videoNumber += 1

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

    def gridPopUp(self):
 
        if self.popUp.isVisible():
            self.popUp.hide()

        else:
            self.popUp.show()

    
    def closeEvent(self, event: QtGui.QCloseEvent):
        """This method handles any cleanup when the application is about to quit.
        
        i.e closing files, releasing threads. 
        """
        
        for camera_thread, processing_thread in self.video_threads:
            logger.info(f"Stopping Camera {camera_thread.camera_index}")
            camera_thread.stop()
            camera_thread.wait()
            processing_thread.stop()
            processing_thread.wait()
        
        print("Closing application")
        # Pass the event back to the normal handler to close the window.
        super().closeEvent(event)
        
    # endregion

#class for grid management pop up window 
class PopUpWindow(QtWidgets.QWidget):
   
    def __init__(self, output2: QtWidgets.QTextEdit, parent = None):
        super().__init__()
        self.output2 = output2
        self.gridNum = 0


        

        # region [Add Widgets]


        vlayout = QtWidgets.QVBoxLayout()
        #hlayout = QtWidgets.QHBoxLayout()
        
        #self.setLayout(hlayout)

        self.labelGrid = QtWidgets.QLabel()
        vlayout.addWidget(self.labelGrid)

        self.gridSpinBox = QtWidgets.QSpinBox()
        self.gridSpinBox.setMinimum(1)
        vlayout.addWidget(self.gridSpinBox)

        self.okBtn = QtWidgets.QPushButton()
        vlayout.addWidget(self.okBtn)

        self.missSlicesLabel = QtWidgets.QLabel()
        vlayout.addWidget(self.missSlicesLabel)

        self.yesBtn = QtWidgets.QPushButton()
        vlayout.addWidget(self.yesBtn)
        self.yesBtn.hide()

        self.noBtn = QtWidgets.QPushButton()
        vlayout.addWidget(self.noBtn)
        self.noBtn.hide()

        self.typeSlicesLabel = QtWidgets.QLabel()
        vlayout.addWidget(self.typeSlicesLabel)
        self.typeSlicesLabel.hide()

        self.typeSlicesLineEdit= QtWidgets.QLineEdit()
        vlayout.addWidget(self.typeSlicesLineEdit)
        self.typeSlicesLineEdit.hide()

        self.okBtn2 = QtWidgets.QPushButton()
        vlayout.addWidget(self.okBtn2)
        self.okBtn2.hide()

        self.setLayout(vlayout)



        

        
        # endregion

        # region [ Set Text ]
        self.labelGrid.setText("Enter grid number:")
        self.okBtn.setText("Ok")
        self.yesBtn.setText("Yes")
        self.noBtn.setText("No")
        self.okBtn2.setText("Ok")
        self.typeSlicesLabel.setText("Type the numbers of the slices that were picked up on grid " + str(self.gridNum) + " separated by a comma (ex: 3, 4, 5).")

        # endregion

        # region [ Signals ]
        self.okBtn.clicked.connect(self.clickOk)
        self.yesBtn.clicked.connect(self.clickYes)
        self.noBtn.clicked.connect(self.clickNo)
        self.okBtn2.clicked.connect(self.clickOk2)
        
        
        # endregion

    def clickOk(self):
        self.gridNum = self.gridSpinBox.value()

        self.missSlicesLabel.setText("The following slices seem to be the slices picked up on the grid: 3, 4, 5. Is this correct?")
        self.yesBtn.show()
        self.noBtn.show()


    def clickYes(self): 
        self.output2.append("Slices 3, 4, and 5 picked up on Grid " + str(self.gridNum))
        self.close()

    def clickNo(self): 
        self.typeSlicesLabel.show()
        self.typeSlicesLineEdit.show()
        self.okBtn2.show()

    def clickOk2(self): 
        self.sliceNums = self.typeSlicesLineEdit.text()
        self.output2.append("Slices " + str(self.sliceNums) + " picked up on Grid " + str(self.gridNum))
        self.close()
        


