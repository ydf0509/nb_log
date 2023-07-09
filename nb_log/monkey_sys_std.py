import os
import sys
import re
from nb_log.file_write import StdFileWritter
from nb_log import nb_log_config_default

stdout_raw = sys.stdout.write
stderr_raw = sys.stderr.write

dele_color_pattern = re.compile('\\033\[.+?m')

sys_std_file_name = os.environ.get('SYS_STD_FILE_NAME', None) or nb_log_config_default.SYS_STD_FILE_NAME
std_writter = StdFileWritter(sys_std_file_name)


def monkey_sys_stdout(msg):
    stdout_raw(msg)
    msg_delete_color = dele_color_pattern.sub('', msg)
    std_writter.write_2_file(msg_delete_color)
    # std_writter.write_2_file(msg)


def monkey_sys_stderr(msg):
    stderr_raw(msg)
    msg_delete_color = dele_color_pattern.sub('', msg)
    std_writter.write_2_file(msg_delete_color)


def patch_sys_std():
    sys.stdout.write = monkey_sys_stdout
    sys.stderr.write = monkey_sys_stderr
