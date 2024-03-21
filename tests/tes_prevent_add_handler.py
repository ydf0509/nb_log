import logging

import nb_log

nb_log.LogManager('name1').prevent_add_handlers()
logging.getLogger()

logging.RootLogger
print(nb_log.log_manager.get_all_logging_name())
nb_log.log_manager.get_all_handlers()
log2 = nb_log.LogManager('name1').get_logger_and_add_handlers()
log2.debug('hi')