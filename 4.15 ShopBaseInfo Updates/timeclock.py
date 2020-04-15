import eventlet
import time
eventlet.monkey_patch()
with eventlet.Timeout(2,False):
     print(1)
     time.sleep(1.5)
     print(2)
     time.sleep(1)
     print(3)
print(4)
 