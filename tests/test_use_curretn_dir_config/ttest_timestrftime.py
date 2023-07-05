
import time

t1 = time.time()
for i in range(100000):
    now = time.strftime('%H:%M:%S')
    print(now)

print(time.time() -t1)