from socket import AF_INET, SOCK_STREAM, socket

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    server_address = ('127.0.0.1', 7777)
    s.connect(server_address)
    raw_input('Press Enter to terminate ...')
    s.close()