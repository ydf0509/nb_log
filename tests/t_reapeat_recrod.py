

import logging

logger= logging.getLogger('abcd')
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.StreamHandler())


logger.error('一句话打印2次')