# Take pictures with webcame to train image classifier model
# By Camden Turnbull with help from dad (Rhet Turnbull)

# import all used code libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import os
from PIL import Image
import re

# this code created by QT Designer to design the user interface
class Ui_MainWindow(object):
    # counter track how many pictures taken
    counter = 0
    # image name to save on disk
    image_name = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonTakePic = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTakePic.setGeometry(QtCore.QRect(10, 70, 113, 32))
        self.buttonTakePic.setObjectName("buttonTakePic")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 480, 71, 20))
        self.label.setObjectName("label")
        self.picLabel = QtWidgets.QLabel(self.centralwidget)
        self.picLabel.setGeometry(QtCore.QRect(350, 50, 371, 371))
        self.picLabel.setText("")
        self.picLabel.setObjectName("picLabel")
        self.comboBoxLegoType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxLegoType.setGeometry(QtCore.QRect(420, 480, 331, 26))
        self.comboBoxLegoType.setObjectName("comboBoxLegoType")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(350, 450, 421, 20))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(16, 38, 50, 10))
        self.label_2.setObjectName("label_2")
        self.comboBoxCamera = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCamera.setGeometry(QtCore.QRect(70, 30, 241, 26))
        self.comboBoxCamera.setObjectName("comboBoxCamera")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #extra setup code
        self.buttonTakePic.clicked.connect(self.take_photo)
        # when button clicked, take picture
        # get list of cameras attached to computer
        self.load_cameras(MainWindow)
        self.comboBoxLegoType.addItems(
            [
                "3001_2x4_Brick",
                "3003_2x2_Brick",
                "3495_2x2_Roof_Tile_Steep_Slopped",
                "3010_1x4_Brick",
                "3009_1x6_Brick",
            ]
        )
        # self.comboBoxLegoType.addItems(
        #     [
        #        "Penny",
        #        "Quarter",
        #        "Dime",
        #        "Nickel"
        #     ]
        # )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonTakePic.setText(_translate("MainWindow", "Take Picture"))
        self.label.setText(_translate("MainWindow", "Lego Type"))
        self.label_2.setText(_translate("MainWindow", "Camera:"))


    # use imagesnap program to get list of cameras
    def load_cameras(self, MainWindow):
        output = subprocess.check_output(
            ["/usr/local/bin/imagesnap", "-l"], universal_newlines=True
        )
        cameras = re.findall(r'\[(.*?)\]\[',output)
        self.comboBoxCamera.addItems(cameras)

    # take pic w/ image snap
    def take_photo(self, MainWindow):
        # takes a photo with imagesnap
        # install with homebrew: brew install imagesnap
        # image is saved as 'snapshot.jpg' in local working directory

        camera = self.comboBoxCamera.currentText()
        lego_type = self.comboBoxLegoType.currentText()

        # format image name to be legotype_00001.jpg etc.
        self.image_name = lego_type + "_" + "{:0>5d}".format(self.counter) + ".jpg"
        self.counter += 1
        # call imagesnap to take pic
        subprocess.call(
            ["/usr/local/bin/imagesnap", "-d", camera, self.image_name]
        )

        # crop the picture to just middle
        crop_image(self.image_name, (420, 0, 1500, 1080), self.image_name)
        myPixmap = QtGui.QPixmap(self.image_name)
        myScaledPixmap = myPixmap.scaled(
            self.picLabel.size(), QtCore.Qt.KeepAspectRatio
        )
        self.picLabel.setPixmap(myScaledPixmap)
        self.imageLabel.setText(self.image_name)

# crop image and save  
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
