from socket import AF_INET, SOCK_STREAM, socket

import responses as rsp
import txteditor

class Client():
    def __init__(self,io):
            #TODO IO is user interface
        self.__io = io

    def connect(self,ip, port):
        '''Connect to server, start game session'''
        self.__s = socket(AF_INET,SOCK_STREAM)
        try:
            self.__s.connect(srv_addr)
            return True
        except soc_err as e:
            print soc_err
        return False
    
    def __login(self, user_name):
        send_message = rsp.MSG_SEP.join([rsp.__GET_FILES] + [user_name])
        print('Sending message: ', send_message)
        self.s.send(send_message)
        print('Message received: ', response_message)
        response_list = response_message.split(rsp.MSG_SEP)
        response_code = response_list[0]
        response_msg = response_list[1]
        return response_code, files
    
    def __session_rcv(self):
        '''Receive the block of data till next block separator'''
        m,b = '',''
        try:
            b = self.__s.recv(BUFFER_SIZE)
            m += b
            while len(b) > 0 and not (b.endswith(MSG_SEP)):
                b = self.__s.recv(BUFFER_SIZE)
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
            
        except soc_err as e:
            if e.errno == 107:
                print 'Server closed connection, terminating ...' 
            else:
                print 'Connection error: %s' % str(e) 
            self.s.close()
            print 'Disconnected'
            m = ''
        return m

    def __protocol_rcv(self,message):
        '''Processe received message:
        server notifications and request/responses separately'''
        print 'processing message'
        return


    def ui_loop(self):
        while True:
            1+1
            #listen to UI
    
    def network_loop(self):
        while True:
            m = self.__session_rcv()
            if len(m) <= 0:
                break
            self.__protocol_rcv(m)
    
    def __close(self):
        self.s.close()

if __name__ == '__main__':
    io = GUI()

    client = Client(io)
    
    

    srv_addr = ('127.0.0.1',7777)

    if client.connect(srv_addr):
        
        ui_thread = Thread(name='UIThread',target=client.ui_loop)
        network_thread = Thread(name='Thread',target=client.network_loop)
             
        ui_thread.start()
        network_thread.start()

        network_thread.join()
        notifications_thread.join()

    print 'Terminating'

    