import json

print('导入nb_log之前的print是普通的')
from nb_log import get_logger
get_logger('lalala3',log_filename='lalala3.log',formatter_template=5,log_file_handler_type=6,is_use_loguru_stream_handler=False)
logger = get_logger('lalala',log_filename='lalala.log',formatter_template=5,log_file_handler_type=6,is_use_loguru_stream_handler=False)
# logger = get_logger('hihihi',)

logger.debug(f'debug是绿色，说明是调试的，代码ok ')
logger.info('info是天蓝色，日志正常 ')
logger.warning('黄色yello，有警告了 ')
logger.error('粉红色说明代码有错误 ')
logger.critical('血红色，说明发生了严重错误 ')
logger.debug({"k":1,'k2':2})
# logger.debug(msg='aaa',extra={"k":1,'k2':2})
print('导入nb_log之后的print是强化版的可点击跳转的')
def func_ya(x):
    print(x)
func_ya('print可以显示是func_ya中的函数打印的')


print('以下是  loguru 的日志色彩模式')
logger_loguru = get_logger('logger_loguru',log_filename='logger_loguru.log',
                           log_file_handler_type=7,is_use_loguru_stream_handler=True)
logger_loguru.debug('loogger use loguru deug')
logger_loguru.info('loogger use loguru info')
logger_loguru.warning('loogger use loguru warning')
logger_loguru.error('loogger use loguru error')
logger_loguru.critical('loogger use loguru critical')
