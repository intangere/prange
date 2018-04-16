import os
import time
import psutil
import sys
import signal
import msgpack

dead = 1
root = os.getpid()
r, w  = None, None
res = None

def collect():
    global res
    res_ = [msgpack.unpackb(x.encode(), raw=True) for x in res.split(',') if x != '']
    res = None
    return res_

def handleSIGCHLD(_, d):
    global dead
    dead += 1

signal.signal(signal.SIGCHLD, handleSIGCHLD) #signal.SIG_IGN)

def context(func):
    def wrapper(*args, **kwargs):
        if not os.getpid() == root:
           result = func(*args, **kwargs)
           f = os.fdopen(w, 'w')
           f.write(msgpack.packb(result).decode() + ',')
           f.close()
           sys.exit(1)
    return wrapper

class Prange(object):
      def __init__(self, limit):
          self.root_pid = os.getpid()
          self.limit = limit + 1
          self.count = 0

          global r, w
          r, w = os.pipe()
          self.f1 = os.fdopen(w, 'w')

      def __iter__(self):
          return self

      def next(self):
          return self.__next__()

      def __next__(self):

          global dead
          self.count += 1
          if os.getpid() == self.root_pid:

             if self.count >= self.limit:
                while dead != self.limit:
                      time.sleep(.001)
                dead = 1
                self.f1.close()
                f = os.fdopen(r)
                global res
                res = f.read()
                f.close()
                raise StopIteration
             else:
                pid = os.fork()
                return

          if self.count >= 2:
             raise StopIteration
