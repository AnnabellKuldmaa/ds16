from socket import AF_INET, SOCK_STREAM, socket

import responses as rsp

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    server_address = ('127.0.0.1', 7777)
    s.connect(server_address)

    s.send('Markus')
    while True:
        message = s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', message)
    s.close()