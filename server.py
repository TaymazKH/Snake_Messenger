from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock, Condition
from socket import socket
from time import sleep
import util

class Server:

    def __init__(self):
        self.pool = ThreadPoolExecutor(5)
        self.connections = []
        self.waiting_to_connect = []
        self.waiting_to_remove = []
        self.waiting_to_modify = False
        self.iterating = 0
        self.wtm_lock = Lock()
        self.i_lock = Lock()
        self.m_cond = Condition()
        self.i_cond = Condition()

    # @util.lock__(lock)
    def handle(self, m0, c0, a0):
        self.wtm_lock.acquire()
        b = self.waiting_to_modify
        self.wtm_lock.release()
        while b:
            self.m_cond.wait()
            self.wtm_lock.acquire()
            b = self.waiting_to_modify
            self.wtm_lock.release()
        self.i_lock.acquire()
        self.iterating += 1
        self.i_lock.release()
        for con in self.connections:
            try:
                if con!=c0:
                    con.send(f"{a0[1]}: {m0}".encode())
            except Exception:
                pass
        self.i_lock.acquire()
        self.iterating -= 1
        self.i_cond.notify_all()
        self.i_lock.release()

    def listen_and_respond(self, c: socket, a):
        try:
            while True:
                msg = c.recv(1024).decode()
                if msg=="":
                    break
                self.pool.submit(self.handle, msg, c, a)
        except Exception:
            pass
        try:
            self.wtm_lock.acquire()
            self.waiting_to_remove.append(c)
            self.wtm_lock.release()
        except KeyboardInterrupt:
            pass

    def collect_garbage(self):
        while True:
            sleep(2)
            self.wtm_lock.acquire()
            m1 = False
            if len(self.waiting_to_remove)!=0:
                self.waiting_to_modify = True
                m1 = True
            self.wtm_lock.release()
            if m1:
                self.i_lock.acquire()
                b1 = self.iterating!=0
                self.i_lock.release()
                while b1:
                    self.i_cond.wait()
                    self.i_lock.acquire()
                    b1 = self.iterating!=0
                    self.i_lock.release()
                for c in self.waiting_to_remove:
                    self.connections.remove(c)
                self.waiting_to_remove.clear()
                self.wtm_lock.acquire()
                self.waiting_to_modify = False
                self.i_cond.notify_all()
                self.wtm_lock.release()
            sleep(2)
            self.wtm_lock.acquire()
            m2 = False
            if len(self.waiting_to_connect)!=0:
                self.waiting_to_modify = True
                m2 = True
            self.wtm_lock.release()
            if m2:
                self.i_lock.acquire()
                b2 = self.iterating!=0
                self.i_lock.release()
                while b2:
                    self.i_cond.wait()
                    self.i_lock.acquire()
                    b2 = self.iterating!=0
                    self.i_lock.release()
                for t in self.waiting_to_connect:
                    h = Thread(target=self.listen_and_respond, args=(t[0], t[1],), daemon=True)
                    h.start()
                    self.connections.append(t[0])
                self.waiting_to_connect.clear()
                self.wtm_lock.acquire()
                self.waiting_to_modify = False
                self.i_cond.notify_all()
                self.wtm_lock.release()

    def start_server(self):
        try:
            host, port = input("address and port: ").split(':')
            port = int(port)
            s = socket()
            s.bind((host, port))
            s.listen()
            Thread(target=self.collect_garbage(), daemon=True).start()
            while True:
                c, a = s.accept()
                self.wtm_lock.acquire()
                self.waiting_to_connect.append((c, a))
                self.wtm_lock.release()
        except KeyboardInterrupt:
            # pool.shutdown(wait=False)
            print("server stopped")

if __name__=="__main__":
    Server().start_server()
