
from nb_log import get_logger


logger = get_logger('abcdcd',
                    log_filename='f4b.log',
                    error_log_filename='f4b_error.log')

logger = get_logger('abcdcd',
                    log_filename='f4b.log',
                    error_log_filename='f4b_error.log')

logger.info('正常日志只写入普通文件')

logger.error('错误日志也要写入普通文件和')

print(logger.handlers)