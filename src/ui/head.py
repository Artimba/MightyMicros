import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os
import cv2
from pathlib import Path


from src.ui.main_ui import Ui_MainWindow
from src.ui.display_write_video_thread import VideoThread
from src import PROJECT_ROOT

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

        self.save_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder to Save Files')
        print(self.save_path)
        #self.save_path = os.path.join(PROJECT_ROOT, 'recordings')
        self.textFileNum = 1
        # self.temp_data = ['data/demo video ui - side angle video slicing.mp4', 'data/demo video ui - microtome camera slicing.mp4']
        # self.temp_data = ['data/output_2.mp4', 'data/output.mp4']

        # Change/add any property about ui here
        self.videoNumber = 1
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.frame_5.setMinimumSize(QtCore.QSize(440, 330))
        self.numSlices = 1
        self.isRecord = False
        
        # region [ Add widgets]
        self.mediaPlayer1 = QMediaPlayer(self.ui.frame_5, QMediaPlayer.VideoSurface)
        self.videoWidget1 = QVideoWidget()
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

        self.outputConsoleBtn = QtWidgets.QPushButton(self.ui.ConFrame)
        self.outputConsoleBtn.setObjectName("outputConsole")
        self.ui.verticalLayout_4.addWidget(self.outputConsoleBtn)

        self.clearConsoleBtn = QtWidgets.QPushButton(self.ui.ConFrame)
        self.clearConsoleBtn.setObjectName("outputConsole")
        self.ui.verticalLayout_4.addWidget(self.clearConsoleBtn)


        self.videoCombo = QtWidgets.QComboBox(self.ui.frame_4)
        self.ui.horizontalLayout_12.addWidget(self.videoCombo)
        
        self.gridBtn = QtWidgets.QPushButton(self.ui.frame_4)
        self.ui.horizontalLayout_12.addWidget(self.gridBtn)
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

        self.ui.horizontalLayout_12.removeWidget(self.ui.toolButton_4)
        self.ui.toolButton_4.deleteLater()
        self.ui.toolButton_4 = None

        self.ui.horizontalLayout_12.removeWidget(self.ui.toolButton_5)
        self.ui.toolButton_5.deleteLater()
        self.ui.toolButton_5= None

        self.ui.horizontalLayout_12.removeWidget(self.ui.toolButton_6)
        self.ui.toolButton_6.deleteLater()
        self.ui.toolButton_6= None

        self.ui.horizontalLayout_10.removeWidget(self.ui.label_5)
        self.ui.label_5.deleteLater()
        self.ui.label_5 = None

        self.ui.horizontalLayout_10.removeWidget(self.ui.label_6)
        self.ui.label_6.deleteLater()
        self.ui.label_6 = None
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
        
        
        self.ui.tabWidget.setCurrentIndex(0)
        
        # region [ Signals ]
        self.timer = QtCore.QTimer()

        
        self.ui.pushButton.clicked.connect(self.ClickBTN)
        self.gridBtn.clicked.connect(self.gridPopUp)
        self.clearConsoleBtn.clicked.connect(self.clickClear)
        self.outputConsoleBtn.clicked.connect(self.clickWrite)
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

        self.InitializeCamera(0, False) # TODO: Switch to false for prod
        self.InitializeCamera(1, True)

        #self.threadBtn1.clicked.connect(self.InitializeCamera)
        #self.threadBtn2.clicked.connect(self.InitializeCamera)
        # endregion
        
        # region [ Translation ]
        _translate = QtCore.QCoreApplication.translate
        self.ui.pushButton_2.setText(_translate("MainWindow", "Play"))
        self.ui.pushButton_5.setText(_translate("MainWindow", "Play"))
        self.ui.label_3.setText(_translate("MainWindow", ""))
        self.ui.label_4.setText(_translate("MainWindow", ""))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.RecordTab), _translate("MainWindow", "Slicing"))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_2), _translate("MainWindow", "Grid Management"))
        self.gridBtn.setText(_translate("MainWindow", "Grid Management"))
        self.ui.label_2.setText(_translate("MainWindow", "External Camera Feed"))
        self.ui.label.setText(_translate("MainWindow", "Microtome Camera Feed"))
        self.clearConsoleBtn.setText(_translate("MainWindow", "Clear"))
        self.outputConsoleBtn.setText(_translate("MainWindow", "Write to File"))

        #self.threadBtn1.setText(_translate("MainWindow", "Show Mighty Micros Camera"))
        #self.threadBtn2.setText(_translate("MainWindow", "Show Microtome Camera"))

        # endregion


        # region [ Aesthetics ]

        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.ui.label.setFont(font)
        self.ui.label_2.setFont(font)
        self.ui.ConTitle.setFont(font)
        self.ui.ConTitle_2.setFont(font)

        font2 = QtGui.QFont()
        font2.setPointSize(18)
        font2.setWeight(50)
        font2.setBold(False)
        font2.setUnderline(False)

        self.ui.pushButton.setFont(font2)
        self.ui.pushButton_2.setFont(font2)
        self.ui.pushButton_5.setFont(font2)
        self.gridBtn.setFont(font2)
        self.clearConsoleBtn.setFont(font2)
        self.outputConsoleBtn.setFont(font2)

        self.output1.setFont(font2)
        self.output2.setFont(font2)


        # endregion

    def InitializeCamera(self, camera_index: int, do_detections=True):
        # Manage unique integers for threads
        
        
        if self.camera_index == 0:
            self.ui.label_3.setText("Loading...")
        elif self.camera_index == 1:
            self.ui.label_4.setText("Loading...")
        elif self.camera_index >= 2:
            # TODO: This is a stopgap since we aren't asking user for camera index. We should be asking for index, not assuming.
            self.video_threads[0].stop()
            self.camera_index = 0
        
        
        # logger.info(f"Initializing Camera {(self.camera_index, self.temp_data[self.camera_index])}")
        logger.info(f"Initializing Camera {self.camera_index}")
        camera_thread = VideoThread(self.camera_index, self.save_path, do_detections=do_detections)
        
        camera_thread.camera_failed_signal.connect(camera_thread.stop)
        camera_thread.frame_signal.connect(lambda image, idx=self.camera_index: self.UpdatePixmap(image, idx))
        camera_thread.console_signal.connect(self.update_console)
        
        camera_thread.start()
                
        self.camera_index += 1
        self.video_threads.append(camera_thread)


        
    
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
            for idx, camera_thread in enumerate(self.video_threads, start=1):
                camera_thread.start_recording(self.videoNumber)
            self.isRecord = True
            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Started")
            self.output2.append("\nRecording Video "+str(self.videoNumber)+" Started")
            
        else:
            
            self.ui.pushButton.setText("Start Recording")
            self.timer.stop()
            [camera_thread.stop_recording() for camera_thread in self.video_threads]
            self.isRecord = False
            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Stopped")
            self.output2.append("\nRecording Video "+str(self.videoNumber)+" Started")
            self.videoCombo.addItem("Recording Session " + str(self.videoNumber))
            
            

            
            self.videoNumber += 1

    def update_console(self, text: str):
        self.output1.append(text)
        # Set output2's text to be the same as output1's
        self.output2.setText(self.output1.toPlainText())

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
        logger.info(f"Loading video {num}")
        logger.info(str(Path(self.save_path, f'video_recording_0_{num}.mp4')))
        self.mediaPlayer1.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(str(Path(self.save_path, f'video_recording_0_{num}.mp4')))))
        self.mediaPlayer2.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(str(Path(self.save_path, f'video_recording_1_{num}.mp4')))))

        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)

        #text = open(os.path.join(self.save_path, f'console_output_{str(self.videoNumber)}.txt'), "r").read()
        #self.output2.append(text)

    def gridPopUp(self):

        self.gridManager = GridManagerPopUp(self.output2, self.output1, '3, 4, 5', self)
 
        if self.gridManager.isVisible():
            self.gridManager.hide()

        else:
            self.gridManager.show()

    def clickClear(self): 
        self.output1.clear() 
        self.output2.clear() 

    def clickWrite(self):
        text = self.output1.toPlainText() 

        with open(os.path.join(self.save_path, f'console_output_{self.textFileNum}.txt'), 'w') as file:
            file.write(text)

        self.textFileNum += 1


    
    def closeEvent(self, event: QtGui.QCloseEvent):
        """This method handles any cleanup when the application is about to quit.
        
        i.e closing files, releasing threads. 
        """
        
        for camera_thread in self.video_threads:
            logger.info(f"Stopping Camera {camera_thread.camera_index}")
            camera_thread.stop()
            camera_thread.wait()
        
        print("Closing application")
        # Pass the event back to the normal handler to close the window.
        super().closeEvent(event)
        

#class for grid management pop up window 
class GridManagerPopUp(QtWidgets.QWidget):
   
    def __init__(self, output2: QtWidgets.QTextEdit, output1: QtWidgets.QTextEdit, missSlices: str, parent = None):
        super().__init__()
        self.output2 = output2
        self.output1 = output1
        self.gridNum = 0

        self.setWindowTitle('Grid Manager')

        self.missSlices = missSlices #the slices that got picked up on the grid (slices that went missing from model's detection database)
        

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
        
        # endregion

        # region [ Signals ]
        self.okBtn.clicked.connect(self.clickOk)
        self.yesBtn.clicked.connect(self.clickYes)
        self.noBtn.clicked.connect(self.clickNo)
        self.okBtn2.clicked.connect(self.clickOk2)
        
        
        # endregion

        # region [ Aesthetics ]
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(50)
        font.setBold(False)
        font.setUnderline(False)

        self.labelGrid.setFont(font)
        self.gridSpinBox.setFont(font)
        self.okBtn.setFont(font)
        self.missSlicesLabel.setFont(font)
        self.yesBtn.setFont(font)
        self.noBtn.setFont(font)
        self.typeSlicesLabel.setFont(font)
        self.typeSlicesLineEdit.setFont(font)
        self.okBtn2.setFont(font)



        # endregion

    def clickOk(self):
        self.gridNum = self.gridSpinBox.value()
        
        #self.typeSlicesLabel.show() 
        #self.typeSlicesLineEdit.show()
        self.missSlicesLabel.setText("The following slices seem to be the slices picked up on the grid: " + self.missSlices + ". Is this correct?")
        self.yesBtn.show()
        self.noBtn.show()
        #self.okBtn2.show()

        


    def clickYes(self): 
        self.output1.append("Slices 3, 4, and 5 picked up on Grid " + str(self.gridNum))
        self.output2.append("Slices 3, 4, and 5 picked up on Grid " + str(self.gridNum))

        
        self.close()

    def clickNo(self): 
        self.typeSlicesLabel.setText("Type the numbers of the slices that were picked up on grid " + str(self.gridNum) + " separated by a comma (ex: 3, 4, 5).")
        self.typeSlicesLabel.show()
        self.typeSlicesLineEdit.show()
        self.okBtn2.show()

    def clickOk2(self): 
        self.sliceNums = self.typeSlicesLineEdit.text()
        self.output1.append("Slices " + str(self.sliceNums) + " picked up on Grid " + str(self.gridNum))
        self.output2.append("Slices " + str(self.sliceNums) + " picked up on Grid " + str(self.gridNum))
        self.close()


#class for pop up to ask for filepath 
# class AskFilePathPopUp(QtWidgets.QWidget):
#     def __init__(self): 
#         super().__init__()
#         self.setWindowTitle('Set Filepath')

#         vlayout = QtWidgets.QVBoxLayout()

#         self.askFilePathLabel = QtWidgets.QLabel()
#         self.askFilePathLabel.setText('Type a filepath to save recordings/files to:')
#         vlayout.addWidget(self.askFilePathLabel)


        
    
        


