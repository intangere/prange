from prange import Prange, context, collect
import time
from random import randint
import sys, os

@context
def SyncroFunc(r):
    time.sleep(r)
    print('Slept for %s' % r)
    return r

if __name__ == '__main__':
    try:
       for _ in Prange(5):
              SyncroFunc(randint(0, 5))
       result = collect()
       print(result)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        except Exception as e:
            print(e)
