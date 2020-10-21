import logging

logger1 = logging.getLogger('a')
logger1.addHandler(logging.StreamHandler())

logger2 = logging.getLogger('a.b')
logger2.addHandler(logging.StreamHandler())

logger2.error(1)