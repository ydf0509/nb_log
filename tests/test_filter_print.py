import sys

import nb_log

logger = nb_log.get_logger('test_name')

str1 = '我们一起练习 阿弥陀佛'
str2 = '啦啦啦德玛西亚'
str3 = '嘻嘻 善哉善哉的'

print(str1)
print(str2)
print(str3)

logger.info(str1)
logger.info(str2)
logger.info(str3)

sys.stdout.write(str1 + '\n')
sys.stdout.write(str2 + '\n')
sys.stdout.write(str3 + '\n')

sys.stderr.write(str1 + '\n')
sys.stderr.write(str2 + '\n')
sys.stderr.write(str3 + '\n')
