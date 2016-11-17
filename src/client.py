from socket import AF_INET, SOCK_STREAM, socket
import sys
sys.path.append('/home/markus/git/ds16/GUI')
import responses as rsp
import txteditor
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets

class Client():
    def __init__(self,io):
            #TODO IO is user interface
        self.__io = io

    def connect(self,srv_addr, user_name):
        '''Connect to server, start game session'''
        self.__s = socket(AF_INET,SOCK_STREAM)
        self.__s.connect(srv_addr)
        response_message = self.__login(user_name)
        self.__protocol_rcv(response_message)

    
    def __login(self, user_name):
        send_message = rsp.MSG_SEP.join([rsp._GET_FILES] + [user_name])
        print('Sending message: ', send_message)
        self.__s.send(send_message)
        response_message = self.__s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', response_message)
        return response_message
    
    def __session_rcv(self):
        '''Receive the block of data till next block separator'''
        m,b = '',''
        try:
            b = self.__s.recv(rsp.BUFFER_SIZE)
            m += b
            while len(b) > 0 and not (b.endswith(rsp.MSG_SEP)):
                b = self.__s.recv(rsp.BUFFER_SIZE)
                m += b
            if len(b) <= 0:
                print 'Socket receive interrupted'  
                self.s.close()
                m = ''
            m = m[:-1]
        except KeyboardInterrupt:
            self.s.close()
            print 'Ctrl+C issued, terminating ...' 
            m = ''
        return m

    def __protocol_rcv(self,message):
        '''Processe received message:
        server notifications and request/responses separately'''
        print("proto recv", message)
        message = message.split(rsp.MSG_SEP)
        req_code = message[0]
        msg_content = message[1:]
        # self.__s.send('asdasd')
        # if req_code == 
        print 'processing message'
        # return


    def ui_loop(self):
         while True:
             1+1
             #listen to UI
    
    def network_loop(self):
        while True:
            print('network loop')
            m = self.__session_rcv()
            if len(m) <= 0:
                break
            self.__protocol_rcv(m)
    
    def __close(self):
         self.s.close()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    io = txteditor.txteditor_GUI(dialog)

    client = Client(None)
    
    

    srv_addr = ('127.0.0.1', 7777)

    client.connect(srv_addr, 'Markus')
        
    ui_thread = Thread(name='UIThread',target=client.ui_loop)
    network_thread = Thread(name='Thread', target=client.network_loop)
         
    ui_thread.start()
    network_thread.start()

    network_thread.join()
    ui_thread.join()
    # TODO

    print 'Terminating'

    