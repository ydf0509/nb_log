# import nb_log
# import time
#
# logger = nb_log.get_logger('dsdsd',_log_filename='dsdsd.log',is_add_stream_handler=False)
#
#
# t1 = time.perf_counter()
# for i in range(100 * 10000):
#     logger.debug('heloo'*10)
# print(time.perf_counter()-t1)
#
#
# # nb_log的 ConcurrentRotatingFileHandlerWithBufferInitiativeWindow windwos 单进程写入100万条 115秒
# #  linux 58秒。
import time
import nb_log
t1 = time.time()
for i in range(10000):
    print(i)
print(time.time()-t1)