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

DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightblue;
    width: 8px;
    margin: 0.5px;
}
"""

COMPLETED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 8px;
    margin: 0.5px;
}
"""

GAUGE = """
import QtQuick 2.2
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

Rectangle {
    width: 80
    height: 200

    Timer {
        running: true
        repeat: true
        interval: 2000
        onTriggered: gauge.value = gauge.value == gauge.maximumValue ? 5 : gauge.maximumValue
    }

    Gauge {
        id: gauge
        anchors.fill: parent
        anchors.margins: 10

        value: 5
        Behavior on value {
            NumberAnimation {
                duration: 1000
            }
        }

        style: GaugeStyle {
            valueBar: Rectangle {
                implicitWidth: 16
                color: Qt.rgba(gauge.value / gauge.maximumValue, 0, 1 - gauge.value / gauge.maximumValue, 1)
            }
        }
    }
}
"""

# class MyProgressBar(QtWidgets.QProgressBar):
#     def __init__(self, parent = None):
#         QtWidgets.QProgressBar.__init__(self, parent)
#         self.setStyleSheet(DEFAULT_STYLE)

#     def setValue(self, value):
#         QtWidgets.QProgressBar.setValue(self, value)
#         if value <= self.maximum():
#             self.setStyleSheet(COMPLETED_STYLE)

class Ui_MainWindow(object):

    counter = 0
    image_name = ""
    model_name = ""

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
        self.label.setGeometry(QtCore.QRect(170, 460, 71, 20))
        self.label.setObjectName("label")

        self.picLabel = QtWidgets.QLabel(self.centralwidget)
        self.picLabel.setGeometry(QtCore.QRect(210, 40, 551, 371))
        self.picLabel.setText("")
        self.picLabel.setObjectName("picLabel")

        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(240, 430, 491, 16))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 500, 71, 20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(170, 540, 71, 20))
        self.label_3.setObjectName("label_3")

        self.textEditPrediction = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEditPrediction.setGeometry(QtCore.QRect(240, 460, 351, 21))
        self.textEditPrediction.setObjectName("textEditPrediction")

        self.textEditProbability = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEditProbability.setGeometry(QtCore.QRect(240, 500, 351, 21))
        self.textEditProbability.setObjectName("textEditProbability")

        self.comboBoxModelName = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxModelName.setGeometry(QtCore.QRect(240, 540, 351, 26))
        self.comboBoxModelName.setObjectName("comboBoxModelName")

        self.buttonPredict = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPredict.setGeometry(QtCore.QRect(20, 80, 113, 32))
        self.buttonPredict.setObjectName("buttonPredict")
        self.buttonPredict.clicked.connect(self.predict)
        self.buttonPredict.setEnabled(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progressBar = MyProgressBar(self.centralwidget)
        # self.progressBar.setGeometry(QtCore.QRect(710, 50, 61, 391))
        # self.progressBar.setProperty("value", 0)
        # self.progressBar.setOrientation(QtCore.Qt.Vertical)
        # self.progressBar.setObjectName("progressBar")

        self.load_model_names(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonTakePic.setText(_translate("MainWindow", "Take Picture"))
        self.label.setText(_translate("MainWindow", "Prediction:"))
        self.label_2.setText(_translate("MainWindow", "Probability:"))
        self.buttonPredict.setText(_translate("MainWindow", "Predict"))
        self.label_3.setText(_translate("MainWindow", "       Model:"))

    def take_photo(self, MainWindow):
        # takes a photo with imagesnap
        # install with homebrew: brew install imagesnap
        # image is saved as 'snapshot.jpg' in local working directory
        self.image_name = "test" + "_" + "{:0>5d}".format(self.counter) + ".jpg"
        self.counter += 1
        subprocess.call(
            ["/usr/local/bin/imagesnap", "-d", "USB 2.0 Camera", self.image_name]
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

        # self.progressBar.setValue(probability*100)
        # self.progressBar.setTextVisible(True)

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
