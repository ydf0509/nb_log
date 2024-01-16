from nb_log import get_logger
from nb_log.log_manager import logger_catch

logger = get_logger('tets_catch_log', is_use_loguru_stream_handler=False)


@logger_catch(logger, reraise=False)
def f(x, y):
    x / y


f(1, 0)
