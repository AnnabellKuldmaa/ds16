import responses as rsp
from PyQt5.QtCore import QThread, pyqtSignal
import traceback


class Client(QThread):

    # Bound signals for sending stuff to main thread.
    # Call emit on these when something needs to be sent
    # Don't forget to connect on main thread
    new_filename = pyqtSignal(list)
    new_filelist = pyqtSignal(list)
    new_text = pyqtSignal(str)
    new_perm = pyqtSignal(str)


    def __init__(self):
        QThread.__init__(self)
        self._s = None # No socket at init

    def connect(self, socket):
        self._s = socket
        print('Socket added to client')
        return

    def _session_rcv(self):
        '''Receive the block of data till next block separator'''
        m, b = '', ''
        try:
            b = self._s.recv(rsp.BUFFER_SIZE)
            m += b
            while len(b) == rsp.BUFFER_SIZE and not b.endswith(rsp.SPACE_INVADER):
                print('Received', b)
                b = self._s.recv(rsp.BUFFER_SIZE)
                m += b
        except Exception:
            traceback.print_exc()
            self._s.close()
            print ('Ctrl+C issued, terminating ...' )
            m = ''
        return m

    def _protocol_rcv(self,message):
        '''Processe received message:
        server notifications and request/responses separately'''
        print("proto recv", message)
        message = rsp.sanitize_message(message)
        print('message')
        print(message)
        req_code = message[0]
        print('req_code')
        print(req_code)
        msg_content = message[1:]
        print('msg_content')
        print(msg_content)
        if req_code == rsp._FILE_NAME:
            self.new_filename.emit(msg_content)
        elif req_code in [rsp._UPDATE_FILE, rsp._FILE_CONTENT]:
            print('client received', msg_content)
            # TODO> SEE TEXTBOX OLEMA DISABLED
            self.new_text.emit(msg_content[0])
        elif req_code == rsp._FILE_LIST:
            self.new_filelist.emit(msg_content)
        elif req_code == rsp._PERM_LIST:
            self.new_perm.emit(msg_content[0])


        print ('processing message')
        # return
    
    def network_loop(self):
        try:
            while True:
                print('network loop')
                m = self._session_rcv()
                if len(m) <= 0:
                    break
                self._protocol_rcv(m)

        except KeyboardInterrupt:
            return

    def __close(self):
        self._s.close()

    def run(self):
        self.network_loop()
