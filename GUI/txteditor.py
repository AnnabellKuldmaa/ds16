from PyQt5 import QtCore, QtGui, QtWidgets
from GUI_client import Ui_MainWindow

class txteditor_GUI(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.main_text_edit.textChanged.connect(self.read_text)
        self.connect_btn.clicked.connect(self.connect_server)
        self.newfile_btn.clicked.connect(self.new_file)
        self.perm_btn.clicked.connect(self.set_permissions)
        self.open_btn.clicked.connect(self.edit_file)


    def connect_server(self):
        print "connecting"
        # call client with proper arguments
        return

    def new_file(self):
        print "new file"
        # create new file on server
        return

    def edit_file(self):
        print "edit file"
        # open selected file for editing
        return

    def set_permissions(self):
        # give edit permissions to users
        print "set permissions"
        return

    def list_files(self):
        #listen to message about new files from client
        return

    def read_text(self):
        txt = self.main_text_edit.toPlainText()
        return txt




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    txteditor = txteditor_GUI(dialog)

    dialog.show()
    sys.exit(app.exec_())