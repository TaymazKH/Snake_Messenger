from socket import socket
from threading import Thread

class Client:
    def __init__(self, a, p):
        self.continue_flag = True
        c = socket()
        c.connect((a, p))
        Thread(target=self.send, args=(c,)).start()
        Thread(target=self.listen, args=(c,)).start()

    def listen(self, c: socket):
        try:
            while self.continue_flag:
                print(c.recv(1024).decode())
        except Exception:
            pass
        self.continue_flag = False
        c.close()

    def send(self, c: socket):
        try:
            while self.continue_flag:
                msg = input()
                c.send(msg.encode())
                if msg=="":
                    break
        except Exception:
            pass
        self.continue_flag = False
        c.close()

if __name__=="__main__":
    address, port = input("address and port: ").split(':')
    port = int(port)
    Client(address, port)
