from socket import AF_INET, SOCK_STREAM, socket
import select
import datetime
from collections import defaultdict

import responses as rsp

file_dict = {} # contains files and their contents

user_dict = defaultdict(set) # contains users and their files
online_clients = {} #clients -> sockets


"""
open_files_dict[filename] = [usernames]
"""
open_files_dict = {}

SOCKET_LIST = []


def get_message(sock):
    message = ''
    while True:
        chunk = sock.recv(rsp.BUFFER_SIZE)
        if not chunk:
            break
        else:
            message += chunk
    return message


def handle_client(sock):
    while True:
        message = get_message(sock)
        message = message.split(rsp.MSG_SEP)
        req_code = message[0]

        if len(message) > 1:
            action = command_dict[req_code]  # Get action from dict
            response = action(message[1:])
        else:
            response = command_dict[message]

        sock.send(response)


def broadcast_file_list(server_socket, sock):
    for client, socket in online_clients.items():
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try:
                socket.send(rsp.MSG_SEP.join([rsp.__FILE_LIST] + user_dict[client]))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def request_user(user_name):
    if user_name in user_dict:  # return file list if username exists
        response = rsp.MSG_SEP.join([rsp.__FILE_LIST] + user_dict[user_name])
    else:  # else add user to dict
        user_dict[user_name] = []
        response = rsp.__RESP_OK
    return response


def edit_file(args):
    """
    Changes contents of the file
    args:
        -file name
        -file content
    """
    file_dict[args[0]] = args[1]
    # TODO:
    # - do broadcast somewhere
    return rsp.MSG_SEP.join([rsp.__RESP_OK])


def create_file():
    if file_dict.keys():
        max_nr = max(file_dict.keys())+1
    else:
        max_nr = 0
    file_dict[str(max_nr)] = ''
    return rsp.MSG_SEP.join([rsp.__FILE_NAME, str(max_nr)])


def open_file(filename):
    return rsp.MSG_SEP.join([rsp.__FILE_CONTENT, file_dict[filename]])


def edit_permission(args):
    """
    args - list of names.
        1. filename
        2-inf. usernames
    """
    filename = args[0]
    userlist = args[1:]
    for u_name in user_dict.keys():
        if u_name in userlist:
            user_dict[u_name].add(filename)
        else:
            try:
                user_dict[u_name].remove(filename)
            except KeyError:
                continue



command_dict = {rsp.__GET_FILES: request_user,
                rsp.__EDIT_FILE: edit_file,
                rsp.__CREATE_FILE: create_file,
                #rsp.__UPDATE_FILE: broadcast,
                rsp.__OPEN_FILE: open_file,
                rsp.__EDIT_PERMISSION: edit_permission}


if __name__ == '__main__':
    print 'Running'
    s = socket(AF_INET, SOCK_STREAM)
    SOCKET_LIST.append(s)
    s.bind(('127.0.0.1', 7777))
    s.listen(1)
    print "Socket is bound to %s:%d" % s.getsockname()
    print 'Socket %s:%d is in listening state' % s.getsockname()
    threads = []
    try:
        while 1:
            ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST,[],[],0)

            for sock in ready_to_read:
                # a new connection request recieved
                if sock == s:
                    sockfd, addr = s.accept()
                    SOCKET_LIST.append(sockfd)
                    u_name = s.recv(rsp.BUFFER_SIZE)
                    online_clients[u_name] = sockfd
                    print "Client (%s, %s) connected" % addr

                else:
                    message = get_message(sock)
                    message = message.split(rsp.MSG_SEP)
                    req_code = message[0]

                    if len(message) > 1:
                        action = command_dict[req_code]  # Get action from dict
                        response = action(message[1:])
                        if req_code == rsp.__CREATE_FILE:
                            broadcast_file_list(s, sock)
                    else:
                        response = command_dict[message]

                    sock.send(response)

                #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            #client_socket, client_addr = s.accept()
            #SOCKET_LIST.append(client_socket)
            #handle_client(client_socket)
            #print 'New client connected from %s:%d' % client_addr
            #print 'Local end-point socket bound on: %s:%d' % client_socket.getsockname()
            # Wait for user input before terminating application

    except KeyboardInterrupt:
        print 'Terminating ...'
        s.close()

