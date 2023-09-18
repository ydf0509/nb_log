
import time
import nb_log

logger=nb_log.get_logger('cc')

t_start = time.time()
for i in range(100000):
    logger.debug(111)
print(time.time() - t_start)