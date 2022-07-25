def server():
    from socket import socket
    s = socket()
    address, port = input("address and port: ").split(':')
    port = int(port)
    s.bind((address, port))
    s.listen()
    c, a = s.accept()
    msg = c.recv(1024)
    msg = msg.decode()
    print(msg)
    c.close()

if __name__=="__main__":
    server()
