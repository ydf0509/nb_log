import traceback

import sys
import logging
import nb_log


logger = nb_log.get_logger('global_except_hook',log_filename='global_except_hook.log')
def global_except_hook(exctype, value, tracebackx):
    # 输出异常信息到日志
    # print(exctype)
    # print(value)
    # print(traceback.format_tb(tracebackx))
    logger.error('Unhandled exception:', exc_info=(exctype, value, tracebackx))

# 设置全局异常钩子
sys.excepthook = global_except_hook



if __name__ == '__main__':
    # 测试异常
    def test_exception():
        try:
            raise ValueError('Test exception')
        except Exception as e:
            pass
            raise OSError('aaaa32') from e


    # 触发异常
    print(ValueError.__name__)
    test_exception()