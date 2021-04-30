import nb_log
import time
t1 = time.time()
import sys

def my_print(x):
    line = sys._getframe().f_back.f_lineno
    # 获取被调用函数所在模块文件名
    file_name = sys._getframe(1).f_code.co_filename

    sys.stdout.write(
        f'{time.strftime("%H:%M:%S")}  "{file_name}￥{line}"   {x}')
    # sys.stdout.write(f'{x}\n')
    # sys.stdout.flush()


for i in range(1000000):
    # print(i,)
    my_print(i)
print('\n')
print(time.time() -t1)