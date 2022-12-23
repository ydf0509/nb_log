from auto_run_on_remote import run_current_script_on_remote
run_current_script_on_remote()
from nb_log import get_logger

logger = get_logger('mylog',log_filename='mylog4.log',log_file_handler_type=2)


for i in range(1):
    logger.error(f'testss {i}')