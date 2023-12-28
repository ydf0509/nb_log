import sys
import time

from nb_log import get_logger

logger = get_logger('lalala',log_filename='lalala.log',formatter_template=7,log_file_handler_type=2)
# logger = get_logger('hihihi',)

logger.debug(f'debug是绿色，说明是调试的，代码ok ')
logger.info('info是天蓝色，日志正常 ')
logger.warning('黄色yello，有警告了 ')
logger.error('粉红色说明代码有错误 ')
logger.critical('血红色，说明发生了严重错误 ')
print('print被自动转化成蓝色')

sys.stdout.write(
                    f'\033[0;37;44m  我我我 \033[0m \n')  # 36  93 96 94



# sys.stdout.write(')

sys.stdout.write("\033[32m这是绿色背景的文本\033[0m")

sys.stdout.write("\033[42m这是绿色背景的文本\033[0m")

sys.stdout.write("\033[0;44m这是绿色背景的文本\033[0m")


sys.stdout.write('\033[0;31m assist_msg\033[0m \033[0;37;41m effective_information_msg\033[0m')


time.sleep(10000)