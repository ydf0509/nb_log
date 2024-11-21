


import logging
import time

logging.basicConfig()

import nb_log
from nb_log import logging_tree_helper

logger = nb_log.get_logger('aaa',log_level_int=10)

# logging.getLogger(None,).setLevel(30)
# nb_log.get_logger(None,log_level_int=30)
logging.warning('cccc')


logger.debug('hiuhihi')


print(logging.getLogger().handlers)
nb_log.logging_tree_helper.printout()


time.sleep(100000)