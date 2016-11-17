from socket import AF_INET, SOCK_STREAM, socket
import sys
sys.path.append('/home/markus/git/ds16/GUI')
import responses as rsp
import txteditor
from threading import Thread
from Queue import Queue
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import time
import traceback
import multiprocessing


class Client():
    def __init__(self,io):
            #TODO IO is user interface

        self._io = io

    def connect(self,srv_addr, user_name):
        '''Connect to server, start game session'''
        self._s = socket(AF_INET,SOCK_STREAM)
        self._s.connect((srv_addr, 7777))
        response_message = self.__login(user_name)
        self.__protocol_rcv(response_message)

    
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
        req_code = message[0]
        msg_content = message[1:].remove(rsp.SPACE_INVADER)
        if req_code == rsp._FILE_NAME:
            self._io.add_file_cbox(msg_content) #Won't send created file

        # self._s.send('asdasd')
        # if req_code == 
        print 'processing message'
        # return


    def ui_loop(self):
         while True:
             1+1
             #listen to UI
    
    def network_loop(self):
        try:
            while True:
                print('network loop')
                m = self._session_rcv()
                if len(m) <= 0:
                    break
                self.__protocol_rcv(m)

        except KeyboardInterrupt:
            return

    def __close(self):
         self._s.close()


class listen_ui(QThread):

    def __init__(self, queue, client):
        QThread.__init__(self)
        self.queue = queue
        self.client = client

    def handle_command(self, command):
        command = command.split(rsp.MSG_SEP)
        if command[0] == rsp._CONNECT:
            self.client.connect(command[1], command[2])
            network_thread = multiprocessing.Process(name='UIThread', target=client.network_loop)
            network_thread.start()
        else:
            self.client._s.send(rsp.MSG_SEP.join(command))
        print('Midagi')

    def run(self):
        while True:
            try:
                command = self.queue.get(block=False)
                self.handle_command(command)
                print('Command received %s' % command)
            except Exception, e:
                #print(e)
                pass

            #time.sleep(0.3)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    dialog.show()

    ui_queue = Queue()
    io = txteditor.txteditor_GUI(dialog, ui_queue)

    client = Client(io)

    #srv_addr = '127.0.0.1'
    #client.connect(srv_addr, 'Markus')


    ui_listener_thread = listen_ui(ui_queue, client)

    ui_listener_thread.start()

    # TODO
    sys.exit(app.exec_())

    print 'Terminating'

    