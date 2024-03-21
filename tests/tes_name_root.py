

import logging

logger = logging.getLogger('')
sh = logging.StreamHandler()
sh.setLevel(10)
logger.addHandler(sh)
logger.setLevel(10)


logger2 = logging.getLogger('p.name2')
# sh = logging.StreamHandler()
# sh.setLevel(10)
# logger2.addHandler(sh)
# logger2.setLevel(40)

logger2.info('222')
logger.debug('1111')
