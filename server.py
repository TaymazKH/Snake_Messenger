def server():
    from socket import socket
    s = socket()
    address, port = input().split(':')
    s.bind((address, int(port)))
    s.listen()
    c, a = s.accept()
    msg = c.recv(1024)
    msg = msg.decode()
    print(msg)
    c.close()

if __name__=="__main__":
    server()
