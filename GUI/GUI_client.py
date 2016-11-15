# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_client.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_text_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.main_text_edit.setGeometry(QtCore.QRect(20, 50, 761, 501))
        self.main_text_edit.setObjectName("main_text_edit")
        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.connect_btn.setObjectName("connect_btn")
        self.newfile_btn = QtWidgets.QPushButton(self.centralwidget)
        self.newfile_btn.setGeometry(QtCore.QRect(340, 10, 75, 23))
        self.newfile_btn.setObjectName("newfile_btn")
        self.perm_btn = QtWidgets.QPushButton(self.centralwidget)
        self.perm_btn.setGeometry(QtCore.QRect(580, 10, 75, 23))
        self.perm_btn.setObjectName("perm_btn")
        self.IP_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.IP_edit.setGeometry(QtCore.QRect(100, 10, 113, 20))
        self.IP_edit.setInputMask("")
        self.IP_edit.setText("")
        self.IP_edit.setObjectName("IP_edit")
        self.user_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.user_edit.setGeometry(QtCore.QRect(220, 10, 113, 20))
        self.user_edit.setObjectName("user_edit")
        self.open_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_btn.setGeometry(QtCore.QRect(500, 10, 75, 23))
        self.open_btn.setObjectName("open_btn")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(420, 10, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.perm_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.perm_edit.setGeometry(QtCore.QRect(660, 10, 113, 20))
        self.perm_edit.setObjectName("perm_edit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
        self.newfile_btn.setText(_translate("MainWindow", "New File"))
        self.perm_btn.setText(_translate("MainWindow", "Permissions"))
        self.IP_edit.setPlaceholderText(_translate("MainWindow", "IP address:port"))
        self.user_edit.setPlaceholderText(_translate("MainWindow", "Username"))
        self.open_btn.setText(_translate("MainWindow", "Edit File"))

