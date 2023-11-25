import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os
import cv2


from src.ui.main_ui import Ui_MainWindow
from src.ui.display_write_video_thread import Thread1, Thread2, Thread3
from src import PROJECT_ROOT
from src.pipeline.detection import Model

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
        self.numSlices = 1
        self.isRecord = False
        
        # region [ Widgets ]

        # region [ Set up camera display ]
        self.camera1 = cv2.VideoCapture(0)
        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.updateFrame1)
        self.timer1.start(30)

        self.camera2 = cv2.VideoCapture(1)
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.updateFrame2)
        self.timer2.start(30)
        # endregion

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
        # endregion
        
        # region [ Translation ]
        _translate = QtCore.QCoreApplication.translate
        self.ui.pushButton_2.setText(_translate("MainWindow", "Play"))
        self.ui.pushButton_5.setText(_translate("MainWindow", "Play"))
        self.ui.label_3.setText(_translate("MainWindow", ""))
        self.ui.label_4.setText(_translate("MainWindow", ""))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.RecordTab), _translate("MainWindow", "Camera Feeds"))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_2), _translate("MainWindow", "Media Players"))

        # endregion
        
     
   
    # region [ Methods ]
    def ImageUpdateSlot1(self, Image): 
        self.ui.label_3.setPixmap(QtGui.QPixmap.fromImage(Image)) 

    def ImageUpdateSlot2(self, Image): 
        self.ui.label_4.setPixmap(QtGui.QPixmap.fromImage(Image)) 

    def ClickBTN(self):
        
        if self.timer.isActive() == False:
            self.ui.pushButton.setText("Stop Recording")  
            self.timer.start() #start the timer

            #start writing the video


            self.Fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.Output1 = cv2.VideoWriter('video_recording_1_'+str(self.videoNumber)+'.mp4', self.Fourcc, 30, (640, 480))

         
            self.Output2 = cv2.VideoWriter('video_recording_2_'+str(self.videoNumber)+'.mp4', self.Fourcc, 15, (640, 480))


            self.ThreadActive = True

            self.isRecord = True
            
            #self.Thread2 = Thread2(self.videoNumber, self.frame2, self)
            #self.Thread2.start() 

            self.output1.append("\nRecording Video "+str(self.videoNumber)+" Started")
            
        else: 
            self.ui.pushButton.setText("Start Recording")
            self.timer.stop() 
            self.isRecord = False
            #self.Thread1.stop()
            #self.Thread2.stop()
            self.Output1.release()
            self.Output2.release()

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

    def updateFrame1(self):
    
        ret, frame = self.camera1.read() #get frame from video feed

        #weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')

        #self.model = Model(weights_path)
        
        if ret: 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #get color image from feed
            frame = cv2.resize(frame, (640, 480))
                

            #results = self.model.predict(frame)
                
            #annotated_frame = results[0].plot(labels=False, masks=False)

            

            #try: 

                #for i, bbox in enumerate(results[0].boxes.xyxy):
                 #   coord = results[0].boxes.xyxy[i].numpy()
                  #  self.output1.append("Slice " + str(self.numSlices) + " at (" + str(coord[0]) + ", "+ str(coord[1]) + ") and (" + str(coord[2]) + ", "+str(coord[3]))
                   # self.numSlices += 1
                    #print(results[0].boxes.xyxy[i])
                    #print(str(results[0].boxes.xyxy[i][0]))
                
            #except IndexError: 
               # pass

            if self.isRecord == True: 
                self.Thread1 = Thread1(self.videoNumber, self.frame1, self.Output1, self)

                self.Thread1.start()

                QtTest.QTest.qWait(1)
                self.Thread1.stop()


        
                

                
            qt_frame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format.Format_RGB888) #convert to a format that qt can read 
            #qt_frame = QtGui.QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QtGui.QImage.Format.Format_RGB888) #convert to a format that qt can read 
            
            qt_frame = qt_frame.scaled(640, 480, QtCore.Qt.AspectRatioMode.KeepAspectRatio) #scale the image 

            #run thread3 here 
            #self.Thread3 = Thread3(frame, self)
            #self.Thread3.start()

            #QtTest.QTest.qWait(1000)


            #self.ImageUpdateSlot1(self.Thread3.frame_edit)
            self.ImageUpdateSlot1(qt_frame)
            #self.Thread3.stop()

            #self.frame1 = annotated_frame
            self.frame1 = frame

        
    
    def updateFrame2(self):
        ret, frame = self.camera2.read() #get frame from video feed

        #weights_path = os.path.join(PROJECT_ROOT, 'pipeline', 'runs', 'detect', 'train3', 'weights', 'best.pt')

        #self.model = Model(weights_path)
        
        if ret: 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #get color image from feed
            frame = cv2.resize(frame, (640, 480))
                
        
            #results = self.model.predict(frame)
                
            #annotated_frame = results[0].plot(labels=False, masks=False)

            if self.isRecord == True: 
                self.Thread2 = Thread1(self.videoNumber, self.frame2, self.Output2, self)

                self.Thread2.start()

                QtTest.QTest.qWait(1)
                self.Thread2.stop()
                
            qt_frame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format.Format_RGB888) #convert to a format that qt can read 
            #qt_frame = QtGui.QImage(annotated_frame.data, annotated_frame.shape[1], annotated_frame.shape[0], QtGui.QImage.Format.Format_RGB888) #convert to a format that qt can read 
            
            qt_frame = qt_frame.scaled(640, 480, QtCore.Qt.AspectRatioMode.KeepAspectRatio) #scale the image 

            self.ImageUpdateSlot2(qt_frame)

            self.frame2 = frame

    
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
          