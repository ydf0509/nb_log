import time
import nb_log
from concurrent.futures import ThreadPoolExecutor



def f():
    for i in range(1000000000):
        time.sleep(0.002)
        print('1'*1000)
        # print(f' {"哈"*30}')


pool = ThreadPoolExecutor(100)

for j in range(100):
    pool.submit(f)