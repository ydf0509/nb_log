import time
from multiprocessing import Process
from nb_log import get_logger

logger = get_logger('abcd',log_filename='abcd.log',is_add_stream_handler=False)

def test():
    while True:
        time.sleep(0.0001) # 就算要模拟多进程，最起码要sleep0.1毫秒，真实情况不可能无间隔一直超高速写日志。
        logger.info("test")


if __name__ == '__main__':
    p = [Process(target=test) for _ in range(5)]

    for i in p:
        i.start()
    for i in p:
        i.join()