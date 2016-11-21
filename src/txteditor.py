from multiprocessing import Queue
from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
import re
import traceback

from PyQt5 import QtWidgets, QtCore

from GUI_client import Ui_MainWindow
from client import Client
import responses as rsp


#from Queue import Queue
class txteditor_GUI(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.current_file = None
        self.is_locked = False

        # tie GUI events to actions defined in methods
        self.main_text_edit.textChanged.connect(self.read_text)
        self.user_edit.textChanged.connect(self.enable_connection_btn)
        self.IP_edit.textChanged.connect(self.enable_connection_btn)
        self.connect_btn.clicked.connect(self.connect_server)
        self.newfile_btn.clicked.connect(self.create_file)
        self.set_perm_btn.clicked.connect(self.set_permissions)
        self.get_perm_btn.clicked.connect(self.get_permissions)
        self.open_btn.clicked.connect(self.edit_file)
        self.open_btn.clicked.connect(self.show_current_file)
        self.comboBox.currentIndexChanged.connect(self.set_buttons_perm)

        self.queue = Queue()
        self.network_thread = Client()

        # Signals from thread
        # Thread emits to these variables. Connection here handles what to call on emit.
        self.network_thread.new_filename.connect(self.add_file_cbox)
        self.network_thread.new_text.connect(self.write_text)
        self.network_thread.new_filelist.connect(self.list_files)
        self.network_thread.new_perm.connect(self.set_perm_text)

    def show_current_file(self):
        curr_file = self.comboBox.currentText()
        self.statusbar.showMessage("Currently open file: "+curr_file)

    def set_buttons_perm(self):
        if self.comboBox.count() > 0:
            self.open_btn.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.get_perm_btn.setEnabled(True)
            self.main_text_edit.setEnabled(True)
            self.set_perm_btn.setEnabled(False)
            self.perm_edit.clear()
            self.perm_edit.setEnabled(False)
        if self.comboBox.count() == 1:
            self.main_text_edit.setEnabled(False)
        elif self.comboBox.count() == 0:
            self.open_btn.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.get_perm_btn.setEnabled(False)



    def enable_connection_btn(self):
        srv_addr = self.IP_edit.text()
        username = self.user_edit.text()

        if len(srv_addr) != 0 and len(username) != 0:
            self.connect_btn.setEnabled(True)
        else:
            self.connect_btn.setEnabled(False)

    def connect_server(self):
        print ("connecting")
        srv_addr = self.IP_edit.text()
        username = self.user_edit.text()
        try:
            self._s = socket(AF_INET, SOCK_STREAM)
            self._s.connect((srv_addr, 7777))
            response_message = self.__login(username)
            self.network_thread.connect(self._s)
            self.network_thread.start()

            if self.comboBox.count() == 0:
                self.newfile_btn.setEnabled(True)
            elif self.comboBox.count() > 0:
                self.comboBox.setEnabled(True)
                self.newfile_btn.setEnabled(True)
                self.open_btn.setEnabled(True)
                self.get_perm_btn.setEnabled(True)

            self.connect_btn.setEnabled(False)
            self.IP_edit.setEnabled(False)
            self.user_edit.setEnabled(False)

            self.network_thread._protocol_rcv(response_message)

        except Exception as e:
            print traceback.print_exc()
        return

    def __login(self, user_name):
        send_message = rsp.make_response([rsp._GET_FILES] + [user_name])
        print('Sending message: ', send_message)
        self._s.send(send_message)
        response_message = self._s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', response_message)
        return response_message

    def create_file(self):
        print ("new file")
        self._s.send(rsp.make_response([rsp._CREATE_FILE]))

        self.comboBox.setEnabled(True)
        self.newfile_btn.setEnabled(True)
        self.open_btn.setEnabled(True)
        self.get_perm_btn.setEnabled(True)


        return

    def edit_file(self):
        print ("edit file")
        # open selected file for editing
        self.current_file = str(self.comboBox.currentText())
        self._s.send(rsp.make_response([rsp._OPEN_FILE, self.current_file]))
        self.main_text_edit.setEnabled(True)
        return

    def set_permissions(self):
        try:
            txt = self.perm_edit.text()
            
            self.perm_edit.clear()
            self.perm_edit.setEnabled(False)
            self.comboBox.setEnabled(True)
            self.newfile_btn.setEnabled(True)
            self.open_btn.setEnabled(True)
            self.get_perm_btn.setEnabled(True)
            self.set_perm_btn.setEnabled(False)
        
            print ("Set permissions", txt)
            permitted_user_list = re.split(r'[,; :]+', txt)
            print('Typed usernames:', txt)
            print('Split usernames:', permitted_user_list)
            permitted_user_list = rsp.make_response(permitted_user_list)
            self._s.send(rsp.make_response([rsp._SET_PERM, str(self.comboBox.currentText()),permitted_user_list]))
        except Exception as e:
            traceback.print_exc()
        return
    
    def set_perm_text(self, txt):
        try:
            print('Ui perm received', txt)
            self.perm_edit.setEnabled(True)
            self.set_perm_btn.setEnabled(True)
            self.perm_edit.setText(txt)
        except Exception as e:
            traceback.print_exc()
        return
        
    
    def get_permissions(self):
        # get permission list, all other functionality disabled
        self.comboBox.setEnabled(False)
        self.newfile_btn.setEnabled(False)
        self.open_btn.setEnabled(False)
        self.get_perm_btn.setEnabled(False)
        self._s.send(rsp.make_response([rsp._GET_PERM, str(self.comboBox.currentText())]))
        print ("get permissions")
        return

    def list_files(self, items):
        self.comboBox.clear()
        self.add_file_cbox(items)
        #TODO:if open close file and update open file
        return

    def add_file_cbox(self, item):
        self.comboBox.addItems(item)
        self.comboBox.update()
        print('Added item to cbox')
        print(item)
        return

    def read_text(self):
        txt = self.main_text_edit.toPlainText()
        if not self.is_locked:
            self._s.sendall(rsp.make_response([rsp._UPDATE_FILE, self.current_file, txt]))
        return


    def write_text(self, txt):
        # txt = (write input here)
        try:
            print('UI RECEIVED txt>', txt)
            self.is_locked = True
            self.main_text_edit.setReadOnly(True)
            self.main_text_edit.setPlainText(txt)
            self.main_text_edit.setReadOnly(False)
            print ('Releasing lock')
            self.is_locked = False
        except Exception as e:
            traceback.print_exc()
        return

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    txteditor = txteditor_GUI(dialog)

    txteditor.connect_btn.setEnabled(False)
    txteditor.main_text_edit.setEnabled(False)
    txteditor.set_perm_btn.setEnabled(False)
    txteditor.get_perm_btn.setEnabled(False)
    txteditor.perm_edit.setEnabled(False)
    txteditor.newfile_btn.setEnabled(False)
    txteditor.comboBox.setEnabled(False)
    txteditor.open_btn.setEnabled(False)

    dialog.show()
    sys.exit(app.exec_())