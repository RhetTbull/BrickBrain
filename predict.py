# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testpic.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import os
from PIL import Image
import turicreate as tc
import sys


class Ui_MainWindow(object):

    counter = 0
    image_name = ''
    model_name = 'topview_17March2019.model'
    #model_name = 'legopics.model'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.buttonTakePic = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTakePic.setGeometry(QtCore.QRect(20, 40, 113, 32))
        self.buttonTakePic.setObjectName("buttonTakePic")
        self.buttonTakePic.clicked.connect(self.take_photo)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 480, 71, 20))
        self.label.setObjectName("label")

        self.picLabel = QtWidgets.QLabel(self.centralwidget)
        self.picLabel.setGeometry(QtCore.QRect(210, 40, 551, 371))
        self.picLabel.setText("")
        self.picLabel.setObjectName("picLabel")

        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(210, 450, 561, 16))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 520, 71, 20))
        self.label_2.setObjectName("label_2")

        self.textEditPrediction = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEditPrediction.setGeometry(QtCore.QRect(240, 480, 351, 21))
        self.textEditPrediction.setObjectName("textEditPrediction")
        
        self.textEditProbability = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEditProbability.setGeometry(QtCore.QRect(240, 520, 351, 21))
        self.textEditProbability.setObjectName("textEditProbability")
        
        self.buttonPredict = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPredict.setGeometry(QtCore.QRect(20, 80, 113, 32))
        self.buttonPredict.setObjectName("buttonPredict")
        self.buttonPredict.clicked.connect(self.predict)
        self.buttonPredict.setEnabled(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonTakePic.setText(_translate("MainWindow", "Take Picture"))
        self.label.setText(_translate("MainWindow", "Prediction:"))
        self.label_2.setText(_translate("MainWindow", "Probability:"))
        self.buttonPredict.setText(_translate("MainWindow", "Predict"))

    def take_photo(self,MainWindow):
        #takes a photo with imagesnap 
        #install with homebrew: brew install imagesnap
        #image is saved as 'snapshot.jpg' in local working directory
        self.image_name = 'test' + "_" + "{:0>5d}".format(self.counter) + ".jpg"
        self.counter += 1
        subprocess.call(['/usr/local/bin/imagesnap', '-d', 'USB 2.0 Camera', self.image_name])
        crop_image(self.image_name, (420,0,1500,1080), self.image_name)
        myPixmap = QtGui.QPixmap(self.image_name)
        myScaledPixmap = myPixmap.scaled(self.picLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.picLabel.setPixmap(myScaledPixmap)
        self.imageLabel.setText(self.image_name)
        self.buttonPredict.setEnabled(True)
        self.textEditPrediction.setPlainText('')
        self.textEditProbability.setPlainText('')

    def predict(self,MainWindow):
        # Load the data
        data = tc.image_analysis.load_images(self.image_name, with_path=True)

        # Create the model
        model = tc.load_model(self.model_name)

        # Save predictions to an SArray
        predictions = model.classify(data)

        self.textEditPrediction.setPlainText(predictions[0]['class'])
        self.textEditProbability.setPlainText("{:.2%}".format(predictions[0]['probability']))
        #for i in range(len(data)):
         #   print(data[i]['path'],",  ", predictions[i])

def crop_image(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

