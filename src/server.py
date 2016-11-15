from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock

import responses as rsp

file_dict = {}
user_dict = {}
online_clients = set()


def handle_client(sock):
    while True:
        message = sock.recv(rsp.BUFFER_SIZE)
        message = message.split(rsp.MSG_SEP)
        req_code = message[0]

        if len(message) > 1:
            action = command_dict[message[0]]  # Get action from dict
            response = action(message[1])
        else:
            response = command_dict[message]

        sock.send(response)


if __name__ == '__main__':
    print 'Running'
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('127.0.0.1', 7777))
    s.listen(1)
    print "Socket is bound to %s:%d" % s.getsockname()
    print 'Socket %s:%d is in listening state' % s.getsockname()
    threads = []
    try:
        while 1:

            client_socket, client_addr = s.accept()
            handle_client(client_socket)
            print 'New client connected from %s:%d' % client_addr
            print 'Local end-point socket bound on: %s:%d' % client_socket.getsockname()
            # Wait for user input before terminating application

    except KeyboardInterrupt:
        print 'Terminating ...'
        s.close()


def request_user(user_name):
    if user_name in user_dict:  # return file list if username exists
        response = rsp.MSG_SEP.join([rsp.__FILES] + user_dict[user_name])
    else:  # else add user to dict
        user_dict[user_name] = []
        response = rsp.__RESP_OK
    return response

def edit_file(filename):
    with open('filename'):



command_dict = {rsp.__GET_FILES: request_user,
                rsp.__EDIT_FILE: edit_file}
