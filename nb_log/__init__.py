import logging
import warnings
import nb_log.add_python_executable_dir_to_path_env
from nb_log.set_nb_log_config import use_config_form_nb_log_config_module
from nb_log import nb_log_config_default

from nb_log.monkey_sys_std import patch_sys_std,stderr_raw,stdout_raw
if nb_log_config_default.SYS_STD_FILE_NAME:
    patch_sys_std()

from nb_log.monkey_std_filter_words import patch_std_filter_words
if nb_log_config_default.FILTER_WORDS_PRINT:
    patch_std_filter_words()

from nb_log.monkey_print import nb_print, patch_print, reverse_patch_print, stdout_write, stderr_write, print_raw, is_main_process, only_print_on_main_process
if nb_log_config_default.AUTO_PATCH_PRINT:
    patch_print()



from nb_log.helpers import generate_error_file_name
from nb_log import handlers
from nb_log.log_manager import (LogManager, LoggerLevelSetterMixin, LoggerMixin, LoggerMixinDefaultWithFileHandler,FileLoggerMixin,
                                MetaTypeLogger,MetaTypeFileLogger,
                                get_logger, get_logger_with_filehanlder,
                                )
from nb_log.loggers_imp.compatible_logger import CompatibleLogger

simple_logger = get_logger('simple')
default_logger = LogManager('default').get_logger_and_add_handlers(do_not_use_color_handler=True, )
defaul_logger = default_logger  # Backward compatibility alias for the misspelled name; removing it would break older funboost versions
default_file_logger = LogManager('default_file_logger').get_logger_and_add_handlers(log_filename='default_file_logger.log')

logger_dingtalk_common = LogManager('dingtalk_common_alert').get_logger_and_add_handlers(
    ding_talk_token=nb_log_config_default.DING_TALK_TOKEN,
    log_filename='dingding_common.log')

from nb_log import global_except_hook
from nb_log.exception_auto_log import LogException

# warnings.simplefilter('always')  # Avoid maintaining __warningregistry__ dict, prevents memory leaks caused by warning.warn
# logging.captureWarnings(True)  # Redirect warning.warn from sys.stderr to logging.
# get_logger('',log_level_int=logging.WARNING,log_filename='root.log')  # py.warnings

from nb_log.root_logger import root_logger


from nb_log.capture_warnings import capture_warnings_with_frequency_control

from nb_log.direct_logger import debug,info,warning,error,exception,critical

if nb_log_config_default.SHOW_NB_LOG_LOGO:
    only_print_on_main_process('\033[0m' + r"""
    
    .__   __. .______           __        ______     _______ 
    |  \ |  | |   _  \         |  |      /  __  \   /  _____|
    |   \|  | |  |_)  |  ______|  |     |  |  |  | |  |  __  
    |  . `  | |   _  <  |______|  |     |  |  |  | |  | |_ | 
    |  |\   | |  |_)  |        |  `----.|  `--'  | |  |__| | 
    |__| \__| |______/         |_______| \______/   \______|      
    
         """ + '\033[0m')

if nb_log_config_default.SHOW_PYCHARM_COLOR_SETINGS:
    en_msg = """\033[0m
        1)When using PyCharm, it is strongly recommended to re-customize the theme colors in PyCharm's console as follows, otherwise the color display may be harsh on the eyes. The colors specified in the code are just approximate red, yellow, blue, and green. The display effect varies across different IDE software, themes, and fonts, so users need to set them up themselves.
        The setup method is: Open PyCharm -> File -> Settings -> Editor -> Color Scheme -> Console Colors, select monokai, click to expand ANSI colors,
        and re-modify 7 custom colors: set Blue to 0454F3, Cyan to 06F0F6, Green to 13FC02, Magenta to ff1cd5, red to F80606, yellow to EAFA04, gray to FFFFFF, and white to FFFFFF.
        Different versions of PyCharm, themes, or IDEs can be set according to the actual console display.

        2)When using tools like xshell or finashell to connect to Linux, you can also customize the theme colors, or use the default colors of the shell connection tool.

        Color effect as shown at https://ibb.co/qRssXTr

        You can modify the default logging behavior when the get_logger method is called without parameters in nb_log_config.py at the root directory of the current project.

        nb_log documentation https://nb-log-doc.readthedocs.io/zh_CN/latest/

        Why set PyCharm terminal colors, explaining why \033 cannot determine the final color https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c1.html#c
        \033[0m
        """
    only_print_on_main_process(en_msg)