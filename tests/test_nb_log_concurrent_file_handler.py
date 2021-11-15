from nb_log import get_logger
from concurrent.futures import ProcessPoolExecutor
logger = get_logger('test_nb_log_conccreent',is_add_stream_handler=False,log_filename='test_nb_log_conccreent.log')


def f(x):
    for i in range(200000):
        logger.warning(f'{x} {i}')

if __name__ == '__main__':
    # 200万条 45秒
    pool = ProcessPoolExecutor(10)
    print('start')
    for i in range(2):
        pool.submit(f,i)
    pool.shutdown()
    print('end')