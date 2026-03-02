
from nb_log import get_logger
from pathlib import Path

logger1 = get_logger('logger1',
                     log_path=Path(Path(__file__).parent,'test_dir1').as_posix(),
                     log_filename='cc.log')

logger2 = get_logger('logger2',
                     log_path=Path(Path(__file__).parent,'test_dir2').as_posix(),
                     log_filename='cc.log')


logger1.info('1111')
logger2.info('2222')



