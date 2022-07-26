from threading import Lock

def lock__(lock: Lock):
    def lock_(func):
        def wrap(*args, **kwargs):
            lock.acquire()
            r = func(*args, **kwargs)
            lock.release()
            return r
        return wrap
    return lock_

