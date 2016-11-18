from socket import AF_INET, SOCK_STREAM, socket
import sys
import os
WORK_DIR = os.getcwd()
import responses as rsp
import txteditor
from threading import Thread
from Queue import Queue
from PyQt5 import  QtWidgets
from PyQt5.QtCore import QThread
import traceback
import multiprocessing


class Client(QThread):
    def __init__(self):
            #TODO IO is user interface
        QThread.__init__(self)
    
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

    def run(self):
        self.network_loop()


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

    def run(self):
        while True:
            try:
                command = self.queue.get(block=False)
                self.handle_command(command)
                print('Command received %s' % command)
            except Exception, e:
                pass



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    dialog.show()

    io = txteditor.txteditor_GUI(dialog, ui_queue)

    client = Client(io)

    #srv_addr = '127.0.0.1'
    #client.connect(srv_addr, 'Markus')


    #ui_listener_thread = listen_ui(ui_queue, client)

    ui_listener_thread.start()

    # TODO
    sys.exit(app.exec_())

    print 'Terminating'

    