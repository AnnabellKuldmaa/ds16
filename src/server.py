from socket import AF_INET, SOCK_STREAM, socket
import select
import datetime
from collections import defaultdict
import traceback
import responses as rsp

file_dict = {} # contains files and their contents

user_dict = defaultdict(set) # contains users and their files
online_clients = {} #clients -> sockets
open_files = defaultdict(list) # filename: [user_sock1, ..]


"""
open_files_dict[filename] = [usernames]
"""
open_files_dict = {}

SOCKET_LIST = []


def get_message(sock):
    message = ''
    chunk = sock.recv(rsp.BUFFER_SIZE)
    message += chunk
    while len(chunk) > 0 and not chunk.endswith(rsp.SPACE_INVADER):
        chunk = sock.recv(rsp.BUFFER_SIZE)
        print('recvd CHUNK', chunk)
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


def create_message(code, msg):

    return rsp.make_response([code] + msg)


def broadcast_file_list(server_socket, sock):
    print('Broadcasting')
    for client, socket in online_clients.items():
        print(client)
        # send the message only to peer
        if socket != server_socket:
            try:
                socket.send(rsp.make_response([rsp._FILE_LIST] + user_dict[client]))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def broadcast_text(server_socket, sock, filename):
    print('Broadcasting')
    print(filename)
    print(open_files[filename])
    for socket in open_files[filename]:
        print(open_files)
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                print('socket send, data>', [rsp._UPDATE_FILE, file_dict[filename]])
                socket.send(rsp.make_response([rsp._UPDATE_FILE, file_dict[filename]]))
            except:
                print('socket send error broadacst text')
                # broken socket connection
                traceback.print_exc()                
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                #del online_clients[socket]


def request_user(user_name):
    if user_name in user_dict:  # return file list if username exists
        response = rsp.make_response([rsp._FILE_LIST] + user_dict[user_name])
    else:  # else add user to dict
        user_dict[user_name] = []
        response = rsp._RESP_OK
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
    return rsp.make_response([rsp._RESP_OK])


def create_file(user_name):
    if file_dict.keys():
        max_nr = max(map(int, file_dict.keys())) + 1
    else:
        max_nr = 0
    file_dict[str(max_nr)] = ''
    user_dict[str(max_nr)].add(user_name)
    print('File created, ', str(max_nr))
    return rsp.make_response([rsp._FILE_NAME, str(max_nr)])


def open_file(filename, sock):
    print('open_file, sock', sock, 'filename', filename)
    for file in open_files:
        print(file)
        if file != filename:
            try:
                print('open_files[file].remove(sock), sock:', sock)
                open_files[file].remove(sock)
            except Exception, e:
                pass

    open_files[filename] += [sock]
    print('open_files', open_files)
    return rsp.make_response([rsp._FILE_CONTENT, file_dict[filename]])


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



command_dict = {rsp._GET_FILES: request_user,
                rsp._EDIT_FILE: edit_file,
                rsp._CREATE_FILE: create_file,
                #rsp._UPDATE_FILE: broadcast,
                rsp._OPEN_FILE: open_file,
                rsp._EDIT_PERMISSION: edit_permission}

import time
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
                # print('sock', sock)
                # a new connection request recieved
                if sock == s:
                    # Login choice
                    sockfd, addr = s.accept()
                    SOCKET_LIST.append(sockfd)
                    message = sockfd.recv(rsp.BUFFER_SIZE)
                    message = message.split(rsp.MSG_SEP)
                    req_code = message[0]
                    u_name = message[1]
                    online_clients[u_name] = sockfd
                    print(online_clients)
                    print "Client (%s, %s) connected" % addr

                    message = rsp.make_response([rsp._FILE_LIST] + list(user_dict[u_name]))
                    sockfd.send(message)

                else:
                    # message = get_message(sock)
                    message = sock.recv(rsp.BUFFER_SIZE)
                    if message:
                        print('SERVER RECEIVENG MSG:', message)
                        message = message.split(rsp.MSG_SEP)
                        req_code = message[0]
                        message = message[1:]


                        if req_code == rsp._CREATE_FILE:
                            u_name = [user for user, socket in online_clients.items() if socket == sock]
                            response = create_file(u_name[0])
                        elif req_code == rsp._OPEN_FILE:
                            response = open_file(message[0], sock)
                        elif req_code == rsp._UPDATE_FILE:
                            file_dict[message[0]] = message[1]
                            broadcast_text(s, sock, message[0])
                            response = rsp.make_response([rsp._RESP_OK])
                        else:
                            continue
                        print(file_dict)

                        sock.send(response)
                    #sock.send('yolo')
                #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
            time.sleep(0.01)
            #client_socket, client_addr = s.accept()
            #SOCKET_LIST.append(client_socket)
            #handle_client(client_socket)
            #print 'New client connected from %s:%d' % client_addr
            #print 'Local end-point socket bound on: %s:%d' % client_socket.getsockname()
            # Wait for user input before terminating application

    except Exception, e:

        print 'Terminating ...'
        print(e)
        traceback.print_exc()
        s.close()

