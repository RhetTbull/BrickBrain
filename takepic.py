# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'takepic.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import os
from PIL import Image


class Ui_MainWindow(object):
    counter = 0

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

        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(210, 450, 561, 16))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")

        self.picLabel = QtWidgets.QLabel(self.centralwidget)
        self.picLabel.setGeometry(QtCore.QRect(210, 40, 551, 381))
        self.picLabel.setText("")
        self.picLabel.setObjectName("picLabel")

        self.comboBoxLegoType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxLegoType.setGeometry(QtCore.QRect(240, 480, 331, 26))
        self.comboBoxLegoType.setObjectName("comboBoxLegoType")

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
        self.label.setText(_translate("MainWindow", "Lego Type"))
        self.comboBoxLegoType.addItems(
            [
                "3001_2x4_Brick",
                "3003_2x2_Brick",
                "3495_2x2_Roof_Tile_Steep_Slopped",
                "3010_1x4_Brick",
                "3009_1x6_Brick",
            ]
        )
        

    def take_photo(self, MainWindow):
        # takes a photo with imagesnap
        # install with homebrew: brew install imagesnap
        # image is saved as 'snapshot.jpg' in local working directory
        lego_type = self.comboBoxLegoType.currentText()
        image_name = lego_type + "_" + "{:0>5d}".format(self.counter) + ".jpg"
        self.counter += 1
        subprocess.call(
            ["/usr/local/bin/imagesnap", "-d", "USB 2.0 Camera", image_name]
        )
        crop_image(image_name, (420, 0, 1500, 1080), image_name)
        myPixmap = QtGui.QPixmap(image_name)
        myScaledPixmap = myPixmap.scaled(
            self.picLabel.size(), QtCore.Qt.KeepAspectRatio
        )
        self.picLabel.setPixmap(myScaledPixmap)
        self.imageLabel.setText(image_name)


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
    # ui.comboBoxLegoType.currentIndex = 0
    sys.exit(app.exec_())
