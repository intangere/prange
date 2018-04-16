# prange
Prange (Py 3.6)<br>
Parallel for-loop written in raw Python.<br>
It's not the best, more of a example on how you could do such a thing.<br>
<h1>Dependencies</h1>
..* msgpack
<h1>Usage</h1>
Label functions you want to use in your loop with @context.<br>
If you need to collect the results at the end call collect().<br>

```
from prange import Prange, context, collect
from random import randint
import sys, os, time

@context
def SyncroFunc(r):
    time.sleep(r)
    print('Slept for %s' % r)
    return r

if __name__ == '__main__':

   for _ in Prange(5):
       SyncroFunc(randint(0, 5))

   result = collect()
   print(result)
```

Certain return types will not work. This library uses a msgpack IPC to collect<br>
each processes return value.<br>
So whatever msgpack supports, this should as well.<br>

