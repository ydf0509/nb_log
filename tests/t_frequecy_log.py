import logging
import time

import nb_log
from nb_log.frequency_control_log import FrequencyControlLog


logger = nb_log.get_logger('fc_log')

for i in range(100):
    time.sleep(1)
    FrequencyControlLog(logger).log(logging.WARN,'aaaaa',interval=10)