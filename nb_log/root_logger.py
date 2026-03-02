import logging

import nb_log
from nb_log import nb_log_config_default

_root_logger = logging.getLogger()
_root_handlers = _root_logger.handlers

new_hanlders = []

# if len(_root_logger.handlers):
#     hdr0 = _root_logger.handlers[0]
#     if type(hdr0) is logging.StreamHandler and not isinstance(hdr0,tuple(logging.StreamHandler.__subclasses__())):
#         # if hdr0.level == logging.NOTSET and hdr0.:
#         _root_logger.handlers.pop(0)
'''
有的人在使用nb_log之前，代码就已经运行了 logging.warning 这样的代码，需要先把之前的stream handler 删除掉，不然重复打印。
'''

for hdr in _root_handlers:
    if type(hdr) is logging.StreamHandler and not isinstance(hdr, tuple(logging.StreamHandler.__subclasses__())):
        print(f'drop root logger handler {hdr}')
        continue
    new_hanlders.append(hdr)

_root_logger.handlers = new_hanlders

# 根日志
root_logger = nb_log.get_logger(None,
                                log_filename=nb_log_config_default.ROOT_LOGGER_FILENAME,
                                error_log_filename=nb_log_config_default.ROOT_LOGGER_FILENAME_ERROR,
                                log_level_int=nb_log_config_default.ROOT_LOGGER_LEVEL)
