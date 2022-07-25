from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock
from socket import socket

pool = ThreadPoolExecutor(5)
connections = []
lock = Lock()

def handle(m0, c0, a0):
    lock.acquire()
    for con in connections:
        try:
            if con!=c0:
                con.send(f"{a0[1]}: {m0}".encode())
        except Exception:
            pass
    lock.release()

def listen_and_respond(c: socket, a):
    try:
        while True:
            msg = c.recv(1024).decode()
            if msg=="":
                break
            pool.submit(handle, msg, c, a)
    except Exception:
        pass
    lock.acquire()
    connections.remove(c)
    lock.release()

def start_server():
    host, port = input("address and port: ").split(':')
    port = int(port)
    s = socket()
    s.bind((host, port))
    s.listen()
    try:
        while True:
            c, a = s.accept()
            lock.acquire()
            connections.append(c)
            lock.release()
            h = Thread(target=listen_and_respond, args=(c, a,), daemon=True)
            h.start()
    except KeyboardInterrupt:
        # pool.shutdown(wait=False)
        print("server stopped")

if __name__=="__main__":
    start_server()
