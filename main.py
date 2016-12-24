import sys
import cv2
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from dialog import Ui_Dialog
import ImageProcessingLibrary

class MyForm(QtGui.QDialog):
    RGBColorFilter = ImageProcessingLibrary.RGBColorFilter()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        ###########################################################
        # Connect Signal
        ###########################################################
        self.ui.horizontalSlider_lowHue.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_lowGreen.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_lowBlue.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_highRed.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_highGreen.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_highBlue.valueChanged.connect(self.updateSlider)

        self.ui.spinBox_lowRed.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_lowGreen.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_lowBlue.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_highRed.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_highGreen.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_highBlue.valueChanged.connect(self.updateSpinboxValue)
        

        self.ui.pushButton_loadImage.clicked.connect(self.openImageFile)

        ###########################################################
        # Initial value 
        ###########################################################
        # Init slider value for high Threshold
        self.ui.horizontalSlider_highRed.setValue(255)
        self.ui.horizontalSlider_highGreen.setValue(255)
        self.ui.horizontalSlider_highBlue.setValue(255)
        # Init line edit
        self.ui.spinBox_highRed.setValue(255)
        self.ui.spinBox_highGreen.setValue(255)
        self.ui.spinBox_highBlue.setValue(255)

        # Set scaled properties
        self.ui.label_initialImage.setScaledContents(True)
        self.ui.label_finalImage.setScaledContents(True)

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateResultImage)
        self.timer.start(500)

        self.isImageValid = False

    def updateResultImage(self):
        low_R = self.ui.horizontalSlider_lowHue.value()
        low_G = self.ui.horizontalSlider_lowGreen.value()
        low_B = self.ui.horizontalSlider_lowBlue.value()
        high_R = self.ui.horizontalSlider_highRed.value()
        high_G = self.ui.horizontalSlider_highGreen.value()
        high_B = self.ui.horizontalSlider_highBlue.value()
        
        # Please note that we send value in RGB format
        # But openCV process in GRB. Additional processing is handled in ImageProcessingLibrary blass
        self.RGBColorFilter.filterImage((low_B, low_G, low_R), (high_B, high_G, high_R))
        self.showFilteredImage()

    def openImageFile(self):
        fileDlg = QFileDialog.getOpenFileName(self, "Open Image", "", "Any file (*.*);;Image file(*.jpg *.gif *.png)")
        if self.RGBColorFilter.loadImage(str(fileDlg)) == False:
            # Add messagebox error message here
            print "Cannot Load Image"
            self.isImageValid = False
        else:
            self.isImageValid = True
            self.showOriginalImage()

    def showAllImage(self):
        if self.isImageValid:
            self.showOriginalImage()
            self.showFilteredImage()

    def showOriginalImage(self):
        if self.isImageValid == True:
            # Convert BGR to RGB
            self.cvOriginalImage = self.RGBColorFilter.getOriginalImage()
            # print self.cvOriginalImage
            self.cvOriginalImage = cv2.cvtColor(self.cvOriginalImage, cv2.COLOR_BGR2RGB)
            # Get image properties
            height, width, byteValue = self.cvOriginalImage.shape

            # Convert to QPixmap
            self.qImageData = QImage(self.cvOriginalImage, width, height, QtGui.QImage.Format_RGB888)
            self.qPixmapData = QtGui.QPixmap.fromImage(self.qImageData)

            # scale and place on label
            self.ui.label_initialImage.setPixmap(self.qPixmapData)

    def showFilteredImage(self):
        if self.isImageValid:
            # Convert BGR to RGB
            self.cvFinalImage = self.RGBColorFilter.getFilteredImage()
            # print self.cvOriginalImage
            self.cvFinalImage = cv2.cvtColor(self.cvFinalImage, cv2.COLOR_BGR2RGB)
            # Get image properties
            height, width, byteValue = self.cvFinalImage.shape

            # Convert to QPixmap
            self.qImageData = QImage(self.cvFinalImage, width, height, QtGui.QImage.Format_RGB888)
            self.qPixmapData = QtGui.QPixmap.fromImage(self.qImageData)

            # scale and place on label
            self.ui.label_finalImage.setPixmap(self.qPixmapData)

    def updateSlider(self):
        # self.ui.lineEdit_lowRed.setValue(str(self.ui.horizontalSlider_lowHue.value()))
        self.ui.spinBox_lowRed.setValue(self.ui.horizontalSlider_lowHue.value())
        self.ui.spinBox_lowGreen.setValue(self.ui.horizontalSlider_lowGreen.value()) 
        self.ui.spinBox_lowBlue.setValue(self.ui.horizontalSlider_lowBlue.value())
        self.ui.spinBox_highRed.setValue(self.ui.horizontalSlider_highRed.value())
        self.ui.spinBox_highGreen.setValue(self.ui.horizontalSlider_highGreen.value())
        self.ui.spinBox_highBlue.setValue(self.ui.horizontalSlider_highBlue.value())  
         
    def updateSpinboxValue(self):
        self.ui.horizontalSlider_lowHue.setValue(self.ui.spinBox_lowRed.value())
        self.ui.horizontalSlider_lowGreen.setValue(self.ui.spinBox_lowGreen.value())
        self.ui.horizontalSlider_lowBlue.setValue(self.ui.spinBox_lowBlue.value())
        self.ui.horizontalSlider_highRed.setValue(self.ui.spinBox_highRed.value())
        self.ui.horizontalSlider_highGreen.setValue(self.ui.spinBox_highGreen.value())
        self.ui.horizontalSlider_highBlue.setValue(self.ui.spinBox_highBlue.value())

    def closeApp(self):
        sys.exit(9)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())