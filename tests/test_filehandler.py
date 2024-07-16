

import nb_log

nb_log.get_logger('name1',log_filename='file_my.log')
nb_log.get_logger('name2',log_filename='file_my.log')




logger1 = nb_log.get_logger('name1',log_filename='file1.log')
logger2 = nb_log.get_logger('name2',log_filename='file2.log')
logger1.warning('写入file1')
logger2.warning('写入file2')