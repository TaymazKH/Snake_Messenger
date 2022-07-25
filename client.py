def client():
    from socket import socket
    s = socket()
    address, port = input().split(':')
    s.connect((address, int(port)))
    s.send(input().encode())
    s.close()

if __name__=="__main__":
    client()
