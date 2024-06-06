import time
import warnings

import nb_log
from nb_log.capture_warnings import capture_warnings_with_frequency_control
import random

capture_warnings_with_frequency_control(True, 5)

for i in range(1000):
    warnings.warn(f'{random.random()}警告1', DeprecationWarning)
    warnings.warn(f'{random.random()}警告2', UserWarning)
    time.sleep(1)
