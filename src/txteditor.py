from PyQt5 import QtCore, QtGui, QtWidgets
from GUI_client import Ui_MainWindow
from Queue import Queue
import responses as rsp
from client import Client, listen_ui
from socket import socket, AF_INET, SOCK_STREAM
import traceback
import sys


class txteditor_GUI(Ui_MainWindow):
    def __init__(self, dialog, queue):
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




    def connect_server(self):
        print "connecting"
        srv_addr = self.IP_edit.text()
        username = self.user_edit.text()
        self._s = socket(AF_INET, SOCK_STREAM)
        self._s.connect((srv_addr, 7777))
        response_message = self.__login(username)
        self.__protocol_rcv(response_message)
        return


    def __login(self, user_name):
        send_message = rsp.MSG_SEP.join([rsp._GET_FILES] + [user_name])
        print('Sending message: ', send_message)
        self._s.send(send_message)
        response_message = self._s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', response_message)
        return response_message

    def _session_rcv(self):
        '''Receive the block of data till next block separator'''
        m,b = '',''
        try:
            b = self._s.recv(rsp.BUFFER_SIZE)
            m += b
            while len(b) == rsp.BUFFER_SIZE and not b.endswith(rsp.SPACE_INVADER):
                print('received', b)
                b = self._s.recv(rsp.BUFFER_SIZE)
                m += b
        except Exception:
            traceback.print_exc()
            self._s.close()
            print 'Ctrl+C issued, terminating ...'
            m = ''
        return m

    def __protocol_rcv(self,message):
        '''Processe received message:
        server notifications and request/responses separately'''
        print("proto recv", message)
        message = message.split(rsp.MSG_SEP)
        print('message')
        print(message)
        req_code = message[0]
        print('req_code')
        print(req_code)
        msg_content = message[1:]
        msg_content.remove(rsp.SPACE_INVADER)
        print('msg_content')
        print(msg_content)
        if req_code == rsp._FILE_NAME:
            self._io.add_file_cbox(msg_content)
        if req_code == rsp._UPDATE_FILE:
            print('client received', msg_content)
            # TODO> SEE TEXTBOX OLEMA DISABLED
            self._io.write_text(msg_content[0])

        # self._s.send('asdasd')
        # if req_code ==
        print 'processing message'
        # return

    def create_file(self):
        print "new file"
        self.queue.put(rsp.MSG_SEP.join([rsp._CREATE_FILE]))
        return

    def edit_file(self):
        print "edit file"
        # open selected file for editing
        self.queue.put(rsp.MSG_SEP.join([rsp._OPEN_FILE, self.current_file]))
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
        self.queue.put(rsp.make_response([rsp._UPDATE_FILE, self.current_file, txt]))
        return

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
    txteditor.main_text_edit.setPlainText('tetessssttt')
    sys.exit(app.exec_())