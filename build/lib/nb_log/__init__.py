from nb_log.set_nb_log_config import use_config_form_nb_log_config_module
from nb_log import nb_log_config_default
from nb_log.monkey_print import nb_print, patch_print, reverse_patch_print,stdout_write,stderr_write,print_raw,is_main_process,only_print_on_main_process
from nb_log.log_manager import LogManager, LoggerLevelSetterMixin, LoggerMixin, LoggerMixinDefaultWithFileHandler, get_logger, get_logger_with_filehanlder

if nb_log_config_default.WARNING_PYCHARM_COLOR_SETINGS:
     only_print_on_main_process(
            """
            1)使用pycharm时候，建议重新自定义设置pycharm的console里面的主题颜色。
            设置方式为 打开pycharm的 file -> settings -> Editor -> Color Scheme -> Console Colors 选择monokai，
            并重新修改自定义6个颜色，设置Blue为1585FF，Cyan为06B8B8，Green 为 05A53F，Magenta为 ff1cd5,red为FF0207，yellow为FFB009。
            如果设置为显示背景色快，由于不同版本的pycahrm或主题，可以根据控制台实际显示设置 White 为 1F1F1F， Black 为 FFFFFF，因为背景色是深色，前景色的文字设置为白色比黑色好。
            
            2)使用xshell或finashell工具连接linux也可以自定义主题颜色，默认使用shell连接工具的颜色也可以。
            
            颜色效果如连接 https://i.niupic.com/images/2020/11/04/8WZf.png
            
            在当前项目根目录的 nb_log_config.py 中可以修改当get_logger方法不传参时后的默认日志行为。
            
            """)

simple_logger = LogManager('simple').get_logger_and_add_handlers()
defaul_logger = LogManager('defaul').get_logger_and_add_handlers(do_not_use_color_handler=True, formatter_template=7)
default_file_logger = LogManager('default_file_logger').get_logger_and_add_handlers(log_filename='default_file_logger.log')

logger_dingtalk_common = LogManager('钉钉通用报警提示').get_logger_and_add_handlers(
    ding_talk_token=nb_log_config_default.DING_TALK_TOKEN,
    log_filename='dingding_common.log')

if nb_log_config_default.AUTO_PATCH_PRINT:
    patch_print()
else:
    reverse_patch_print()
