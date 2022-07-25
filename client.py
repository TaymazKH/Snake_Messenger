def client():
    from socket import socket
    s = socket()
    address, port = input("address and port: ").split(':')
    port = int(port)
    s.connect((address, port))
    s.send(input().encode())
    s.close()

if __name__=="__main__":
    client()
