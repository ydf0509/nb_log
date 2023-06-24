import logging
import time

import concurrent_log_handler

def log_file_namer(logger_name: str) -> str:
    # path/name.log.N
    print('logger_name:',logger_name)
    logger_name, backup_number = logger_name.rsplit(".", maxsplit=1)
    # path/name.log
    logger_name = logger_name.replace(".log", "")
    # curr_date = date.today().strftime("%Y_%m_%d")  # noqa: DTZ011
    curr_date = time.strftime("%Y_%m_%d_%H_%M_%S")  # noqa: DTZ011

    return f"{logger_name}_{curr_date}_({backup_number}).log"


# Now for the meat of your program...
logger = logging.getLogger("MyExample")
logger.setLevel(logging.DEBUG)  # optional to set this level here

handler = concurrent_log_handler.ConcurrentTimedRotatingFileHandler(
    filename="/pythonlogs/logger_name_testc.log", mode="a", maxBytes=5, backupCount=6,when='s',
)
# handler.namer = log_file_namer
logger.addHandler(handler)

for idx in range(0, 500):
    time.sleep(0.1)
    print("Loop %d; logging a message." % idx)
    logger.debug("%d > A debug message.", idx)
    if idx % 2 == 0:
        logger.info("%d > An info message.", idx)
print("Done with example; exiting.")