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
                                                                              log_filename='test_nb_log_conccreent56.log', log_file_handler_type=2,
                                                                          # log_path='/root/pythonlogs'
                                                                          )

logger.warning('xxxx'*1000)

def f(x):
    for i in range(20000000):
        # time.sleep(0.01)
        logger.warning(f'{os.getpid()} {x} {i}  ')

# logger.warning('aaaaa')
if __name__ == '__main__':
    # run_current_script_on_remote()
    # 200万条 45秒

    pool = ProcessPoolExecutor(5)
    print('start')
    for i in range(5):
        pool.submit(f,i)
    pool.shutdown()
    print('end')