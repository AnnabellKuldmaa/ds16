import sys
from PyQt5 import QtWidgets, QtCore
from GUI_client import Ui_MainWindow
from Queue import Queue
import responses as rsp
from client import Client
from socket import socket, AF_INET, SOCK_STREAM
import traceback
import time



class txteditor_GUI(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.current_file = '0'

        # tie GUI events to actions defined in methods
        self.main_text_edit.textChanged.connect(self.read_text)
        self.connect_btn.clicked.connect(self.connect_server)
        self.newfile_btn.clicked.connect(self.create_file)
        self.perm_btn.clicked.connect(self.set_permissions)
        self.open_btn.clicked.connect(self.edit_file)

        self.queue = Queue()
        self.network_thread = Client()

        # Signals from thread
        self.network_thread.new_filename.connect(self.add_file_cbox)
        #self.connect(self.thread, SIGNAL("terminated()"), self.updateUi)


    def connect_server(self):
        print "connecting"
        srv_addr = self.IP_edit.text()
        username = self.user_edit.text()
        self._s = socket(AF_INET, SOCK_STREAM)
        self._s.connect((srv_addr, 7777))
        response_message = self.__login(username)
        self.network_thread.connect(self._s)
        self.network_thread.start()

        self.network_thread._protocol_rcv(response_message)

        return

    def __login(self, user_name):
        send_message = rsp.MSG_SEP.join([rsp._GET_FILES] + [user_name])
        print('Sending message: ', send_message)
        self._s.send(send_message)
        response_message = self._s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', response_message)
        return response_message

    def create_file(self):
        print "new file"
        self._s.send(rsp.make_response([rsp._CREATE_FILE]))
        return

    def edit_file(self):
        print "edit file"
        # open selected file for editing
        self._s.send(rsp.MSG_SEP.join([rsp._OPEN_FILE, self.current_file]))
        self.main_text_edit.setEnabled(True)
        return

    def set_permissions(self):
        # give edit permissions to users
        print "set permissions"
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
        self._s.send(rsp.make_response([rsp._UPDATE_FILE, self.current_file, txt]))
        return

    def block_writes(self):
        self.main_text_edit.setEnabled(False)
        time.sleep(0.5)
        self.main_text_edit.setEnabled(True)

    def write_text(self, txt):
        # txt = (write input here)
        print('UI RECEIVED txt>', txt)
        self.main_text_edit.setPlainText(txt)

        return

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    txteditor = txteditor_GUI(dialog)
    dialog.show()
    sys.exit(app.exec_())