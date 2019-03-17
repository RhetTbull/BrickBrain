# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'takepic.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonTakePic = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTakePic.setGeometry(QtCore.QRect(20, 40, 113, 32))
        self.buttonTakePic.setObjectName("buttonTakePic")
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.QRect(170, 20, 571, 391))
        # self.graphicsView.setObjectName("graphicsView")
        self.picLabel =  QtWidgets.QLabel(self.centralwidget)
        self.picLabel.setGeometry(QtCore.QRect(170, 20, 571, 391))
        self.legoNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.legoNameEdit.setGeometry(QtCore.QRect(240, 440, 321, 21))
        self.legoNameEdit.setObjectName("legoNameEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 440, 71, 20))
        self.label.setObjectName("label")
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    myPixmap = QtGui.QPixmap('snapshot.jpg')
    myScaledPixmap = myPixmap.scaled(ui.picLabel.size(), QtCore.Qt.KeepAspectRatio)
    ui.picLabel.setPixmap(myScaledPixmap)
    sys.exit(app.exec_())

