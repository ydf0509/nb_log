import sys
import nb_log
import threading
import time
logger = nb_log.get_logger('hi',formatter_template=7,log_filename='a.log',is_add_stream_handler=False)
# logger = nb_log.get_logger('hi',formatter_template=7)
nb_log.reverse_patch_print()
t1 = time.time()
for i in range(200000):
    # time.sleep(0.01)
    pass
    # logger.debug(f''' {threading.active_count()}    {threading.current_thread()}''')
#     logger.debug(f'''
# 如前所述，用空间去换时间，好处是降低了延时，提升了吞吐，但劣势就在于你需要处理cache的更新并且维护一致性。目前Kafka是怎么更新cache的？简单来说，就是通过发送异步更新请求(UpdateMetadata request)来维护一致性的。既然是异步的，那么在某一个时间点集群上所有broker的cache信息就未必是严格相同的。只不过在实际使用场景中，这种弱一致性似乎并没有太大的问题。原因如下：1. clients并不是时刻都需要去请求元数据的，且会缓存到本地；2. 即使获取的元数据无效或者过期了，clients通常都有重试机制，可以去其他broker上再次获取元数据; 3. cache更新是很轻量级的，仅仅是更新一些内存中的数据结构，
# ''')
#     logger.debug(f''' {i} ''')
#     print(i)
    sys.stdout.write(f'{i}')
print()
print(time.time() -t1)


# import logging
# import time
# t1= time.time()
#
# logger = logging.getLogger('cc')
# fh = logging.FileHandler('cc.log')
# fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
# logger.addHandler(fh)
#
#
# sh = logging.StreamHandler()
# sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
# logger.addHandler(sh)
# for i in range(100000):
#     logger.warning(i)
#
# print(time.time()-t1)