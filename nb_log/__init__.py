from nb_log.set_nb_log_config import use_config_form_nb_log_config_module
from nb_log import nb_log_config_default

from nb_log.monkey_sys_std import patch_sys_std
if nb_log_config_default.SYS_STD_FILE_NAME:
    patch_sys_std()

from nb_log.monkey_std_filter_words import patch_std_filter_words
if nb_log_config_default.FILTER_WORDS_PRINT:
    patch_std_filter_words()

from nb_log.monkey_print import nb_print, patch_print, reverse_patch_print, stdout_write, stderr_write, print_raw, is_main_process, only_print_on_main_process
if nb_log_config_default.AUTO_PATCH_PRINT:
    patch_print()




from nb_log import handlers
from nb_log.log_manager import LogManager, LoggerLevelSetterMixin, LoggerMixin, LoggerMixinDefaultWithFileHandler, get_logger, get_logger_with_filehanlder


simple_logger = get_logger('simple')
defaul_logger = LogManager('defaul').get_logger_and_add_handlers(do_not_use_color_handler=True, formatter_template=7)
default_file_logger = LogManager('default_file_logger').get_logger_and_add_handlers(log_filename='default_file_logger.log')

logger_dingtalk_common = LogManager('钉钉通用报警提示').get_logger_and_add_handlers(
    ding_talk_token=nb_log_config_default.DING_TALK_TOKEN,
    log_filename='dingding_common.log')


from nb_log.direct_logger import debug,info,warning,error,exception,critical

only_print_on_main_process('\033[0m' + r"""

.__   __. .______           __        ______     _______ 
|  \ |  | |   _  \         |  |      /  __  \   /  _____|
|   \|  | |  |_)  |  ______|  |     |  |  |  | |  |  __  
|  . `  | |   _  <  |______|  |     |  |  |  | |  | |_ | 
|  |\   | |  |_)  |        |  `----.|  `--'  | |  |__| | 
|__| \__| |______/         |_______| \______/   \______|      

     """ + '\033[0m')

if nb_log_config_default.SHOW_PYCHARM_COLOR_SETINGS:
    only_print_on_main_process(
        """\033[0m
        1)使用pycharm时候，强烈建议按下面的重新自定义设置pycharm的console里面的主题颜色，否则颜色显示瞎眼，代码里面规定的颜色只是大概的红黄蓝绿。在不同的ide软件和主题、字体下是不同的显示效果，需要用户自己设置。
        设置方式为 打开pycharm的 file -> settings -> Editor -> Color Scheme -> Console Colors 选择monokai，点击展开 ANSI colors，
        并重新修改自定义7个颜色，设置Blue为 0454F3 ，Cyan为 06F0F6 ，Green 为 13FC02 ，Magenta为 ff1cd5 ,red为 F80606 ，yellow为 EAFA04 ，gray 为 FFFFFF ，white 为 FFFFFF 。
        不同版本的pycahrm或主题或ide，可以根据控制台根据实际显示设置。

        2)使用xshell或finashell工具连接linux也可以自定义主题颜色，默认使用shell连接工具的颜色也可以。

        颜色效果如连接 https://ibb.co/qRssXTr

        在当前项目根目录的 nb_log_config.py 中可以修改当get_logger方法不传参时后的默认日志行为。

        nb_log文档 https://nb-log-doc.readthedocs.io/zh_CN/latest/

        为什么要设置pycharm终端颜色，解释为什么\\033不能决定最终颜色 https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c1.html#c
        \033[0m

        """)






