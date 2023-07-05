
import time

t1 = time.time()
for i in range(10000):
    print(time.strftime('%H:%M:%S'))

print(time.time() -t1)