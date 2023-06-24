import time

# from auto_run_on_remote import run_current_script_on_remote
# run_current_script_on_remote()
from nb_log import get_logger

logger = get_logger('mylog',log_filename='mylog4g.log',log_file_handler_type=1,is_add_stream_handler=False)

print('start')
for i in range(200000):
    logger.error(f'testss {i}')
print('over')
