import traceback

import sys
import logging
import nb_log


logger = nb_log.get_logger('global_except_hook',log_filename='global_except_hook.log')
def global_except_hook(exctype, value, tracebackx):
    # Log unhandled exceptions
    # print(exctype)
    # print(value)
    # print(traceback.format_tb(tracebackx))
    logger.error('Unhandled exception:', exc_info=(exctype, value, tracebackx))

# Set global exception hook
sys.excepthook = global_except_hook



if __name__ == '__main__':
    # Test exception
    def test_exception():
        try:
            raise ValueError('Test exception')
        except Exception as e:
            pass
            raise OSError('aaaa32') from e


    # Trigger exception
    print(ValueError.__name__)
    test_exception()