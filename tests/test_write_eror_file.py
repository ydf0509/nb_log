
from nb_log import get_logger


logger = get_logger('abcdcd',
                    log_filename='f5b.log',
                    # error_log_filename='f4b_error.log'
                    )

# logger = get_logger('abcdcd',
#                     log_filename='f4b.log',
#                     error_log_filename='f4b_error.log')

logger.info('正常日志入普通文件和错误文件')

logger.error('错误日志写入单独写入错误文件')

print(logger.handlers)