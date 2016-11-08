from socket import AF_INET, SOCK_STREAM, socket

import responses as rsp

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    server_address = ('127.0.0.1', 7777)
    s.connect(server_address)

    while True:
        send_message = raw_input()
        print('Sending message: ', send_message)
        s.send(send_message)
        received_message = s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', received_message)
    s.close()