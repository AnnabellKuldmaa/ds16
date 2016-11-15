from socket import AF_INET, SOCK_STREAM, socket

import responses as rsp

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    server_address = ('127.0.0.1', 7777)
    s.connect(server_address)

    while True:
        user_name = raw_input()
        send_message = rsp.MSG_SEP.join([rsp.__GET_FILES] + [user_name])
        print('Sending message: ', send_message)
        s.send(send_message)
        response_message = s.recv(rsp.BUFFER_SIZE)
        print('Message received: ', response_message)
        response_list = response_message.split(rsp.MSG_SEP)
        response_code = response_list[0]
        response_msg = response_list[1]
        if response_code == rsp._FILE_LIST:
            continue
            print 'Received file list'
            
    s.close()
    