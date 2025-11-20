

import logging
import time



logger1 =   logging.getLogger('t1')
logger1.setLevel(logging.INFO)
logger1.addHandler(logging.StreamHandler())

logger1.info('xixi')
time.sleep(1)

from nb_log import get_logger

logger2 = get_logger('t1')

print(logger2.handlers)

logger1.info('xixi')
time.sleep(1)
logger2.info('xixi')
