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
If logging.warning() was called before importing nb_log, a default StreamHandler may already exist.
Remove it to prevent duplicate output.
'''

for hdr in _root_handlers:
    if type(hdr) is logging.StreamHandler and not isinstance(hdr, tuple(logging.StreamHandler.__subclasses__())):
        print(f'drop root logger handler {hdr}')
        continue
    new_hanlders.append(hdr)

_root_logger.handlers = new_hanlders

# Root logger
root_logger = nb_log.get_logger(None,
                                log_filename=nb_log_config_default.ROOT_LOGGER_FILENAME,
                                error_log_filename=nb_log_config_default.ROOT_LOGGER_FILENAME_ERROR,
                                log_level_int=nb_log_config_default.ROOT_LOGGER_LEVEL)
