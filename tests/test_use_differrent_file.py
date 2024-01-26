# import logging
# from nb_log import get_logger
# from loguru import logger
#
# # nb_log 写入不同的文件是根据日志命名空间 name 来区分的。方便。
# logger_a = get_logger('a',log_level_int=logging.DEBUG)
# logger_b = get_logger('b',log_level_int=logging.INFO)
# logger_a.debug("嘻嘻a debug会显示")
# logger_a.info("嘻嘻a info会显示")
# logger_b.debug("嘻嘻b debug不会显示")
# logger_b.info("嘻嘻b info会显示")
#
# logger_a.setLevel()
# logger_a.addHandler()
#
# # loguru 不同功能为了写入不同的文件，需要设置消息前缀标志。不方便。
# logger.add('./log_files/c.log',filter=lambda x: '[特殊标志c!]' in x['message'],level='DEBUG')
# logger.add('./log_files/d.log',filter=lambda x: '[特殊标志d!]' in x['message'],level='INFO')
# logger.debug('[特殊标志c!] 嘻嘻c 会显示') #   消息为了控制台显示级别需要带消息标志
# logger.info('[特殊标志c!] 嘻嘻c 会显示') #  消息为了控制台显示级别需要带消息标志
# logger.debug('[特殊标志d!] 嘻嘻d 不会显示') #  消息为了控制台显示级别需要带消息标志
# logger.info('[特殊标志d!] 嘻嘻d') #  消息为了控制台显示级别需要带消息标志
#
# logger.se
#
#
#
# # # nb_log 写入不同的文件是根据日志命名空间 name 来区分的。方便。
# # logger_a = get_logger('a',_log_filename='a.log',log_path='./log_files')
# # logger_b = get_logger('b',_log_filename='b.log',log_path='./log_files')
# # logger_a.info("嘻嘻a")
# # logger_b.info("嘻嘻b")
# #
# # # loguru 不同功能为了写入不同的文件，需要设置消息前缀标志。不方便。
# # logger.add('./log_files/c.log', filter=lambda x: '[特殊标志c!]' in x['message'])
# # logger.add('./log_files/d.log', filter=lambda x: '[特殊标志d!]' in x['message'])
# # logger.add('./log_files/e.log', )
# # logger.info('[特殊标志c!] 嘻嘻c') # 出现在c.log和 e.log  消息为了写入不同文件需要带消息标志
# # logger.info('[特殊标志d!] 嘻嘻d') # 出现在d.log和 e.log  消息为了写入不同文件需要带消息标志
#






# from nb_log import get_logger,LogManager
#
# # logger_a = get_logger('a',_log_filename='ax.log',log_path='./log_files')
# logger_a = LogManager('a').get_logger_and_add_handlers(_log_filename='ax2.log',log_path='./log_files')
# logger_a.info("嘻嘻a")


# from pathlib import Path
# print((Path(__file__).parent.parent.parent.absolute()) / Path('pylogs'))


import logging
from logging import handlers

logger_raw = logging.getLogger("test_logging")

logger_raw.warning('日志太简单太丑了，并且没记录到文件')

# 添加控制台日志
handler_console = logging.StreamHandler()
formatter1 = logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
handler_console.setFormatter(formatter1)
logger_raw.addHandler(handler_console)

# 添加文件日志handler
handler_file = logging.handlers.RotatingFileHandler('test_logging.log',mode='a')
formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S")
handler_file.setFormatter(formatter2)
logger_raw.addHandler(handler_file)


logger_raw.error("日志现在格式变好了，并且记录到文件了")


