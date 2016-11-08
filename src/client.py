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
        response_message = s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', response_message)
        response_list = response_message.split(rsp.MSG_SEP)
        response_code = response_list[0]
        response_msg = response_list[1]
        if response_code == rsp.__RESP_OK:
            continue
        if response_code == rsp.__FILES:
            print('Files you can edit: ', response_msg)
    s.close()