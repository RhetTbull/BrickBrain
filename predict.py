# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testpic.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import subprocess
import os
from PIL import Image
import turicreate as tc
import sys
import re

class Ui_MainWindow(object):

    counter = 0
    image_name = ""
    model_name = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonTakePic = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTakePic.setGeometry(QtCore.QRect(10, 80, 113, 32))
        self.buttonTakePic.setObjectName("buttonTakePic")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 460, 71, 20))
        self.label.setObjectName("label")
        self.picLabel = QtWidgets.QLabel(self.centralwidget)
        self.picLabel.setGeometry(QtCore.QRect(380, 10, 401, 401))
        self.picLabel.setText("")
        self.picLabel.setObjectName("picLabel")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(380, 430, 411, 20))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(370, 500, 71, 20))
        self.label_2.setObjectName("label_2")
        self.textEditPrediction = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEditPrediction.setGeometry(QtCore.QRect(440, 460, 351, 21))
        self.textEditPrediction.setObjectName("textEditPrediction")
        self.textEditProbability = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEditProbability.setGeometry(QtCore.QRect(440, 500, 351, 21))
        self.textEditProbability.setObjectName("textEditProbability")
        self.buttonPredict = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPredict.setGeometry(QtCore.QRect(10, 120, 113, 32))
        self.buttonPredict.setObjectName("buttonPredict")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(370, 540, 71, 20))
        self.label_3.setObjectName("label_3")
        self.comboBoxModelName = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxModelName.setGeometry(QtCore.QRect(440, 540, 351, 26))
        self.comboBoxModelName.setObjectName("comboBoxModelName")
        self.comboBoxCamera = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCamera.setGeometry(QtCore.QRect(70, 20, 291, 26))
        self.comboBoxCamera.setObjectName("comboBoxCamera")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(20, 20, 71, 20))
        self.labelCamera.setObjectName("labelCamera")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # extra setup
        self.buttonPredict.clicked.connect(self.predict)
        self.buttonPredict.setEnabled(False)
        self.load_model_names(MainWindow)
        self.load_cameras(MainWindow)
        self.buttonTakePic.clicked.connect(self.take_photo)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonTakePic.setText(_translate("MainWindow", "Take Picture"))
        self.label.setText(_translate("MainWindow", "Prediction:"))
        self.label_2.setText(_translate("MainWindow", "Probability:"))
        self.buttonPredict.setText(_translate("MainWindow", "Predict"))
        self.label_3.setText(_translate("MainWindow", "       Model:"))
        self.labelCamera.setText(_translate("MainWindow","Camera:"))

    def load_cameras(self, MainWindow):
        output = subprocess.check_output(
            ["/usr/local/bin/imagesnap", "-l"], universal_newlines=True
        )
        cameras = re.findall(r'\[(.*?)\]\[',output)
        self.comboBoxCamera.addItems(cameras)

    def take_photo(self, MainWindow):
        # takes a photo with imagesnap
        # install with homebrew: brew install imagesnap
        # image is saved as 'snapshot.jpg' in local working directory

        camera = self.comboBoxCamera.currentText()
        self.image_name = "test" + "_" + "{:0>5d}".format(self.counter) + ".jpg"
        self.counter += 1
        subprocess.call(
            ["/usr/local/bin/imagesnap", "-d", camera, self.image_name]
        )
        crop_image(self.image_name, (420, 0, 1500, 1080), self.image_name)
        myPixmap = QtGui.QPixmap(self.image_name)
        myScaledPixmap = myPixmap.scaled(
            self.picLabel.size(), QtCore.Qt.KeepAspectRatio
        )
        self.picLabel.setPixmap(myScaledPixmap)
        self.imageLabel.setText(self.image_name)
        self.buttonPredict.setEnabled(True)
        self.textEditPrediction.setPlainText("")
        self.textEditProbability.setPlainText("")

    def predict(self, MainWindow):
        self.model_name = self.comboBoxModelName.currentText()
        # Load the data
        data = tc.image_analysis.load_images(self.image_name, with_path=True)

        # Create the model
        model = tc.load_model(self.model_name)

        # Save predictions to an SArray
        predictions = model.classify(data)

        class_name = predictions[0]["class"]
        probability = predictions[0]["probability"]
        self.textEditPrediction.setPlainText(class_name)
        self.textEditProbability.setPlainText(
            "{:.2%}".format(probability)
        )
        
    def load_model_names(self, MainWindow):
        subfolders = [
            f.name for f in os.scandir(".") if f.is_dir() and ".model" in f.name
        ]
        self.comboBoxModelName.addItems(subfolders)


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
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
