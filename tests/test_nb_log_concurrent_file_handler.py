import os
import time
import sys
# sys.path.insert(0,'/home/ydf/pycodes/nb_log/')
print(sys.path)
from nb_log import get_logger,LogManager
from concurrent.futures import ProcessPoolExecutor
# logger = get_logger('test_nb_log_conccreent',is_add_stream_handler=False,log_filename='test_nb_log_conccreent45.log',log_file_handler_type=1)



from auto_run_on_remote import run_current_script_on_remote

logger = LogManager('test_nb_log_conccreent').get_logger_and_add_handlers(is_add_stream_handler=False,
                                                                              log_filename='test_nb_log_conccreent556k.log', log_file_handler_type=6,
                                                                          # log_path='/root/pythonlogs'
                                                                          )

# logger.warning('xxxx')

def f(x):
    for i in range(10000):
        time.sleep(0.0001)
        logger.warning(f'{os.getpid()} {x} {i}  哈哈哈')

# logger.warning('aaaaa')
if __name__ == '__main__':
    # run_current_script_on_remote()
    # 200万条 45秒
    pass

    pool = ProcessPoolExecutor(5)
    print('start')
    for i in range(5):
        pool.submit(f,i)
    # pool.shutdown()
    # print('end')

    # time.sleep(2)