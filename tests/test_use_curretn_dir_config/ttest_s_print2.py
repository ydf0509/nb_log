
# from nb_log.simple_print import sprint
import time
import datetime
import sys
str1 = ''' 2023-07-05 10:48:35 - lalala - "D:/codes/funboost/test_frame/test_nb_log/log_example2.py:15" - <module> - ERROR - 粉红色说明代码有错误。 粉红色说明代码有错误。 粉红色说明代码有错误。 粉红色说明代码有错误。'''
import logging


print(time.gmtime())
t1 = time.time()
def f():
    for i in range(10000):
        fra = sys._getframe(1)
        line = fra.f_lineno
        file_name = fra.f_code.co_filename
        fun = fra.f_code.co_name



        # print(file_name,line,fun,str1*3,flush=False)
        sys.stdout.write(str([time.strftime('%H:%M:%S'),file_name,line,fun,str1*0]) + '\n')
        # sys.stdout.write(str([time.time(), file_name, line, fun, str1 * 0]) + '\n')
        sys.stdout.flush()
f()

print(time.time() -t1)