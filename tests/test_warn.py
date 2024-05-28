import sys
import warnings
import logging
# logging.captureWarnings(True)
# # logging.debug('aaa')
# warnings.simplefilter('always')
# import nb_log
# nb_log.get_logger('',log_level_int=logging.WARNING)

logging.getLogger('asd').info(66666666)

warnings.warn('sss',DeprecationWarning,1)
warnings.warn('sss',DeprecationWarning,1)

print(sys.__dict__)