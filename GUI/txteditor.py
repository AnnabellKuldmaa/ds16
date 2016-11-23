from PyQt5 import QtCore, QtGui, QtWidgets
from GUI_client import Ui_MainWindow
import sys
import os
WORK_DIR = os.getcwd()
sys.path.append(os.path.join([WORK_DIR, 'src']))
#sys.path.append('../src')
import responses as rsp


class txteditor_GUI(Ui_MainWindow):
    def __init__(self, dialog, queue):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.queue = queue
        self.current_file = '0'

        # tie GUI events to actions defined in methods
        self.main_text_edit.textChanged.connect(self.read_text)
        self.connect_btn.clicked.connect(self.connect_server)
        self.newfile_btn.clicked.connect(self.create_file)
        self.perm_btn.clicked.connect(self.set_permissions)
        self.open_btn.clicked.connect(self.edit_file)

    def connect_server(self):
        print ("connecting")
        socket_info = self.IP_edit.text()
        username = self.user_edit.text()
        self.queue.put(rsp.MSG_SEP.join([rsp._CONNECT, socket_info, username]))
        #self.queue.put(rsp.MSG_SEP.join([rsp._GET_FILES, ]))
        # send command to client with username and socket address:port as arguments
        return

    def create_file(self):
        print ("new file")
        self.queue.put(rsp.MSG_SEP.join([rsp._CREATE_FILE]))
        return

    def edit_file(self):
        print ("edit file")
        # open selected file for editing
        self.queue.put(rsp.MSG_SEP.join([rsp._OPEN_FILE, self.current_file]))
        return

    def set_permissions(self):
        # give edit permissions to users
        print ("set permissions")
        return

    def list_files(self):
        # listen to message about new files from client
        return

    def add_file_cbox(self, item):
        self.comboBox.addItems(item)
        self.comboBox.update()
        print('Added item to cbox')
        print(item)
        return

    def read_text(self):
        txt = self.main_text_edit.toPlainText()
        self.queue.put(rsp.make_response([rsp._UPDATE_FILE, self.current_file, txt]))
        return

    def write_text(self, txt):
        # txt = (write input here)
        print('UI RECEIVED txt>', txt)
        self.main_text_edit.setPlainText(txt)
        return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    txteditor = txteditor_GUI(dialog)
    dialog.show()
    txteditor.main_text_edit.setPlainText('tetessssttt')
    sys.exit(app.exec_())