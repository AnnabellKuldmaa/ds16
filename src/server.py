from socket import AF_INET, SOCK_STREAM, socket

if __name__ == '__main__':
    print 'Running'
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('127.0.0.1', 7777))
    print "Socket is bound to %s:%d" % s.getsockname()
    backlog = 0
    s.listen(backlog)
    print 'Socket %s:%d is in listening state' % s.getsockname()
    client_socket,client_addr = s.accept()
    print 'New client connected from %s:%d' % client_addr
    print 'Local end-point socket bound on: %s:%d' % client_socket.getsockname()
    # Wait for user input before terminating application
    raw_input('Press Enter to terminate ...')
    s.close()
    print 'Terminating ...'