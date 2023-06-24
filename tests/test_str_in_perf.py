import time

str1 = '''
(192.168.43.162,SC-202202121439)-[p20300_t2898176036000] 2023-05-13 19:59:00 - CeleryConsumer--celery_q3 - "celery_consumer.py:172" - DEBUG -  这条消息是 celery 从 celery_q3 队列中取出 ,是由 celery 框架调度 f1 函数处理: args:  () ,  kwargs: {'x': 105, 'y': 210}
19:59:03  "D:\codes\funboost\test_frame\test_broker_celery\test_celery_consume2.py:16"   哈哈哈 105 210
 [2023-05-13 19:59:03,248: INFO/MainProcess] Task celery_q3[celery_q3_result:8e5f8526-0174-456c-a95f-ae6b82c662a9] succeeded in 3.0319999999919673s: 315
(192.168.43.162,SC-202202121439)-[p20300_t2898176994112] 2023-05-13 19:59:05 - CeleryConsumer--celery_q3 - "celery_consumer.py:172" - DEBUG -  这条消息是 celery 从 celery_q3 队列中取出 ,是由 celery 框架调度 f1 函数处理: args:  () ,  kwargs: {'x': 106, 'y': 212}
19:59:08  "D:\codes\funboost\test_frame\test_broker_celery\test_celery_consume2.py:16"   哈哈哈 106 212
'''

t1 = time.time()
for i in range(1000000):
    strx = f'{i}dsfdsf二位热污染看过的广泛地dgdgtrrt烦得很规范化股份将基于人体我看我oiytrbhhttr台湾人提问题{i}'
    boolx = strx in str1


print(time.time() - t1)