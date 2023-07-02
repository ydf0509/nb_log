import sys
from nb_log import nb_log_config_default


def _need_filter_print(msg: str):
    for strx in nb_log_config_default.FILTER_WORDS_PRINT:
        if strx in str(msg):
            return True  # 过滤掉需要屏蔽的打印
    return False


sys_stdout_write_raw = sys.stdout.write
sys_stderr_write_raw = sys.stderr.write


def _sys_stdout_write_monkey(msg: str):
    if _need_filter_print(msg):
        return
    else:
        sys_stdout_write_raw(msg)


def _sys_stderr_write_monkey(msg: str):
    if _need_filter_print(msg):
        return
    else:
        sys_stderr_write_raw(msg)

def patch_std_filter_words():
    sys.stdout.write = _sys_stdout_write_monkey  # 对 sys.stdout.write 打了猴子补丁。使得可以过滤包含指定字符串的消息。
    sys.stderr.write = _sys_stderr_write_monkey
