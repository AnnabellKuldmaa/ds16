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
        MainWindow.resize(934, 660)

        # Main window
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Text edit box
        self.main_text_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.main_text_edit.setGeometry(QtCore.QRect(20, 50, 891, 581))
        self.main_text_edit.setObjectName("main_text_edit")

        # Connection button
        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.connect_btn.setObjectName("connect_btn")

        # New file button
        self.newfile_btn = QtWidgets.QPushButton(self.centralwidget)
        self.newfile_btn.setGeometry(QtCore.QRect(340, 10, 75, 23))
        self.newfile_btn.setObjectName("newfile_btn")

        # Set permissions button
        self.set_perm_btn = QtWidgets.QPushButton(self.centralwidget)
        self.set_perm_btn.setGeometry(QtCore.QRect(680, 10, 91, 23))
        self.set_perm_btn.setObjectName("set_perm_btn")

        # Get permissions button
        self.get_perm_btn = QtWidgets.QPushButton(self.centralwidget)
        self.get_perm_btn.setGeometry(QtCore.QRect(590, 10, 91, 23))
        self.get_perm_btn.setObjectName("get_perm_btn")

        # IP address textbox
        self.IP_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.IP_edit.setGeometry(QtCore.QRect(100, 10, 113, 20))
        self.IP_edit.setInputMask("")
        self.IP_edit.setText("127.0.0.1")
        self.IP_edit.setObjectName("IP_edit")

        # Username textbox
        self.user_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.user_edit.setGeometry(QtCore.QRect(220, 10, 113, 20))
        self.user_edit.setObjectName("user_edit")

        # Open file button
        self.open_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_btn.setGeometry(QtCore.QRect(500, 10, 75, 23))
        self.open_btn.setObjectName("open_btn")

        # File list combobox
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(420, 10, 69, 22))
        self.comboBox.setObjectName("comboBox")

        # Permissions textbox
        self.perm_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.perm_edit.setGeometry(QtCore.QRect(780, 10, 131, 21))
        self.perm_edit.setObjectName("perm_edit")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cooperative editor"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
        self.newfile_btn.setText(_translate("MainWindow", "New File"))
        self.set_perm_btn.setText(_translate("MainWindow", "Set permissions"))
        self.IP_edit.setPlaceholderText(_translate("MainWindow", "IP address:port"))
        self.user_edit.setPlaceholderText(_translate("MainWindow", "Username"))
        self.open_btn.setText(_translate("MainWindow", "Edit File"))
        self.perm_edit.setPlaceholderText(_translate("MainWindow", "Users with permissions"))
        self.get_perm_btn.setText(_translate("MainWindow", "Get permissions"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

