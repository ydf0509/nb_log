import json

print('导入nb_log之前的print是普通的')
from nb_log import get_logger
get_logger('lalala3',log_filename='lalala3.log',formatter_template=7,log_file_handler_type=6,is_use_loguru_stream_handler=False)
logger = get_logger('lalala',log_filename='lalala.log',formatter_template=7,log_file_handler_type=6,is_use_loguru_stream_handler=False)
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
