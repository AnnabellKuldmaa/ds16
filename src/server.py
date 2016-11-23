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


def broadcast_file_list(server_socket, sock):
    print('Broadcasting')
    for client, socket in online_clients.items():
        print(client)
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                print('socket send, data>', [rsp._FILE_LIST, list(user_dict[client])])
                socket.send(rsp.make_response([rsp._FILE_LIST] + list(user_dict[client])))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                remove_user_presence(sock)


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

                # broken socket, remove it
                remove_user_presence(sock)


def edit_file(args):
    """
    Changes contents of the file
    args:
        -file name
        -file content
    """
    file_dict[args[0]] = args[1]
    return rsp.make_response([rsp._RESP_OK])


def create_file(user_name):
    if file_dict.keys():
        max_nr = max(map(int, file_dict.keys())) + 1
    else:
        max_nr = 0
    file_dict[str(max_nr)] = ''
    user_dict[user_name].add(str(max_nr))
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
            except Exception as e:
                pass

    open_files[filename] += [sock]
    print('open_files', open_files)
    return rsp.make_response([rsp._FILE_CONTENT, file_dict[filename]])


def get_perm(filename):
    user_list = []
    for u_name in user_dict.keys():
        if filename in user_dict[u_name]:
            user_list.append(u_name)
    print('User list', user_list)
    return rsp.make_response([rsp._PERM_LIST] + user_list)
    

def edit_permission(args):
    """
    args - list of names.
        1. filename
        2-inf. usernames
    """
    filename = args[0]
    userlist = args[1:]
    if rsp.SPACE_INVADER in userlist:
        userlist.remove(rsp.SPACE_INVADER)
    print ('Editing permissions for file', filename)
    print ('New user list', userlist)
    for u_name in user_dict.keys():
        if u_name in userlist:
            user_dict[u_name].add(filename)
        else:
            try:
                user_dict[u_name].remove(filename)
            except KeyError:
                continue
    # Also add permissions to users not yet seen by the server
    for u_name in userlist:
        if u_name not in user_dict:
            user_dict[u_name].add(filename)
    print (user_dict)


def remove_user_presence(sock):
    # Remove client from online clients
    for client, socket in online_clients.items():
        if socket == sock:
            del online_clients[client]
    # Remove client from list of users having a file open
    for filename, socket_list in open_files.items():
        if socket in socket_list:
            socket_list.remove(socket)
    # Remove client from SOCKET_LIST
    try:
        SOCKET_LIST.remove(sock)
    except ValueError:
        pass

    socket.close()


import time
if __name__ == '__main__':
    print ('Running')
    s = socket(AF_INET, SOCK_STREAM)
    SOCKET_LIST.append(s)
    s.bind(('127.0.0.1', 7777))
    s.listen(1)
    print ("Socket is bound to %s:%d" % s.getsockname())
    print ('Socket %s:%d is in listening state' % s.getsockname())
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
                    print ('Tulen!')
                    message = sockfd.recv(rsp.BUFFER_SIZE)  # We assume username is shorter than buffer
                    message = rsp.sanitize_message(message)
                    req_code = message[0]
                    u_name = message[1]

                    if u_name in online_clients:
                        message = rsp.make_response([rsp._USERNAME_TAKEN])
                        sockfd.send(message)
                        break

                    SOCKET_LIST.append(sockfd)
                    online_clients[u_name] = sockfd
                    print(online_clients)
                    print ("Client (%s, %s) connected" % addr)
                    print(user_dict)
                    message = rsp.make_response([rsp._FILE_LIST] + list(user_dict[u_name]))
                    sockfd.send(message)

                else:
                    # message = get_message(sock)
                    #Is message coming from that socket
                    message = sock.recv(rsp.BUFFER_SIZE)
                    final_message = message
                    if message:
                        #is message ended
                        while len(message) == rsp.BUFFER_SIZE and not message.endswith(rsp.SPACE_INVADER):
                            message = sock.recv(rsp.BUFFER_SIZE)
                            final_message += message
                            
                        message = final_message
                        print('SERVER RECEIVENG MSG:', message)
                        message = rsp.sanitize_message(message)
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
                        elif req_code == rsp._GET_PERM:
                            response = get_perm(message[0])
                        elif req_code == rsp._SET_PERM:
                            edit_permission(message)
                            broadcast_file_list(s, sock)
                            client = [client for client, socket in online_clients.items() if socket == sock][0]
                            print('NEW LIST FOR CLIENT:', client, user_dict[client])
                            response = rsp.make_response([rsp._FILE_LIST] + list(user_dict[client]))

                            #TODO brodcast new file list
                        else:
                            continue
                        print(file_dict)

                        sock.send(response)
                    else:
                        remove_user_presence(sock)
                        print('User disconnected. Presence removed.')
            time.sleep(0.01)

    except Exception as e:

        print ('Terminating ...')
        print(e)
        traceback.print_exc()
        s.close()

