from nb_log import nb_log_config_default


def _need_filter_print(msg: str):
    for strx in nb_log_config_default.FILTER_WORDS_PRINT:
        if strx in str(msg):
            return True  # 过滤掉需要屏蔽的打印
    return False
