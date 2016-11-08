from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock

import responses as rsp


file_dict = {}
user_dict = {}


def handle_client(sock):
    user_name = sock.recv()
    if user_name:
        if user_name in user_dict:  # return file list if username exists
            response = rsp.MSG_SEP.join([rsp.__FILE_LIST] + user_dict[user_name])
        else:  # else add user to dict
            user_dict[user_name] = []
            response = rsp.__NEW_USER
        sock.send(response)
    else:  # return if empty string sent
        return

    while True:
        message = sock.recv()


if __name__ == '__main__':
    print 'Running'
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('127.0.0.1', 7777))
    print "Socket is bound to %s:%d" % s.getsockname()
    print 'Socket %s:%d is in listening state' % s.getsockname()
    threads = []
    while True:

        client_socket, client_addr = s.accept()
        handle_client(client_socket)
        print 'New client connected from %s:%d' % client_addr
        print 'Local end-point socket bound on: %s:%d' % client_socket.getsockname()
        # Wait for user input before terminating application

    raw_input('Press Enter to terminate ...')
    s.close()
    print 'Terminating ...'