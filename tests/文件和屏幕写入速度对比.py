

import time

# 打印到屏幕
start_time = time.time()
for i in range(1000000):
    print(str(i) * 100,end='\n')  # end='' 避免换行
print("Time for print:", time.time() - start_time)

# 写入文件
start_time = time.time()
with open('output.txt', 'w') as f:
    for i in range(1000000):
        f.write(str(i) * 100 + '\n')
print("Time for file write:", time.time() - start_time)