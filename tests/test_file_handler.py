import time

# from auto_run_on_remote import run_current_script_on_remote
# run_current_script_on_remote()
from nb_log import get_logger

logger = get_logger('mylog',log_filename='mylog4g.log',log_file_handler_type=6,is_add_stream_handler=False)
get_logger('mylog2',log_filename='mylog4g3.log',log_file_handler_type=6,is_add_stream_handler=False)
print('start')
t1 = time.time()
for i in range(20000):
    logger.error(f'testss {i}')
print(time.time() -t1)
print('over')
