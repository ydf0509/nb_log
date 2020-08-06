# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/4/11 0011 0:56
"""

使用覆盖的方式，做配置。
"""
import sys
import time
import importlib
from pathlib import Path
from nb_log import nb_log_config_default


# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring
def nb_print(*args, sep=' ', end='\n', file=None):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        sys.stderr.write(sep.join(args))  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。

    else:
        # 获取被调用函数在被调用时所处代码行数
        line = sys._getframe().f_back.f_lineno
        # 获取被调用函数所在模块文件名
        file_name = sys._getframe(1).f_code.co_filename
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        if nb_log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
            sys.stdout.write(
                f'\033[0;34m{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   \033[0;30;44m{sep.join(args)}\033[0m{end} \033[0m')  # 36  93 96 94
        else:
            sys.stdout.write(
                f'\033[0;34m{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end} \033[0m')  # 36  93 96 94
        # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')


def show_nb_log_config():
    nb_print('显示nb_log 包的默认的低优先级的配置参数')
    for var_name in dir(nb_log_config_default):
        nb_print(var_name, getattr(nb_log_config_default, ':', var_name))
    print('\n')


config_file_content = '''# -*- coding: utf-8 -*-
"""
此文件nb_log_config.py是自动生成到python项目的根目录的。
在这里面写的变量会覆盖此文件nb_log_config_default中的值。对nb_log包进行默认的配置。

由于不同的logger天然就是多个实例，所以可以通过get_logger_and_handlers传参针对每个logger精确的做不同的配置。
最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
重要的重复三遍。

"""
import logging
# 
# DING_TALK_TOKEN = '3dd0eexxxxxadab014bd604XXXXXXXXXXXX'  # 数据组报警机器人
# 
# EMAIL_HOST = ('smtp.sohu.com', 465)
# EMAIL_FROMADDR = 'aaa0509@sohu.com'  # 'matafyhotel-techl@matafy.com',
# EMAIL_TOADDRS = ('cccc.cheng@silknets.com', 'yan@dingtalk.com',)
# EMAIL_CREDENTIALS = ('aaa0509@sohu.com', 'abcdefg')
# 
# ELASTIC_HOST = '127.0.0.1'
# ELASTIC_PORT = 9200
# 
# KAFKA_BOOTSTRAP_SERVERS = ['192.168.199.202:9092']
# ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT = False
# 
# MONGO_URL = 'mongodb://myUserAdmin:mimamiama@127.0.0.1:27016/admin'
# 
# DEFAULUT_USE_COLOR_HANDLER = True  # 是否默认使用有彩的日志。有的人讨厌彩色可以关掉（主要是不按提示的说明配置pycahrm的conose）。
# DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True     # 在控制台是否显示彩色块状的日志。为False则不使用大块的背景颜色。
# AUTO_PATCH_PRINT = True  # 是否自动打print的猴子补丁，如果打了猴子补丁，print自动变色和可点击跳转。
# WARNING_PYCHARM_COLOR_SETINGS = True
# 
# DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False  # 是否默认同时将日志记录到记log文件记事本中。
# LOG_FILE_SIZE = 100  # 单位是M,每个文件的切片大小，超过多少后就自动切割
# LOG_FILE_BACKUP_COUNT = 3
# 
# LOG_LEVEL_FILTER = logging.DEBUG  # 默认日志级别，低于此级别的日志不记录了。例如设置为INFO，那么logger.debug的不会记录，只会记录logger.info以上级别的。
# RUN_ENV = 'test'
# 
# FORMATTER_DICT = {
#     1: logging.Formatter(
#         '日志时间【%(asctime)s】 - 日志名称【%(name)s】 - 文件【%(filename)s】 - 第【%(lineno)d】行 - 日志等级【%(levelname)s】 - 日志信息【%(message)s】',
#         "%Y-%m-%d %H:%M:%S"),
#     2: logging.Formatter(
#         '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
#         "%Y-%m-%d %H:%M:%S"),
#     3: logging.Formatter(
#         '%(asctime)s - %(name)s - 【 File "%(pathname)s", line %(lineno)d, in %(funcName)s 】 - %(levelname)s - %(message)s',
#         "%Y-%m-%d %H:%M:%S"),  # 一个模仿traceback异常的可跳转到打印日志地方的模板
#     4: logging.Formatter(
#         '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
#         "%Y-%m-%d %H:%M:%S"),  # 这个也支持日志跳转
#     5: logging.Formatter(
#         '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
#         "%Y-%m-%d %H:%M:%S"),  # 我认为的最好的模板,推荐
#     6: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
#                          "%Y-%m-%d %H:%M:%S"),
#     7: logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S"),  # 一个只显示简短文件名和所处行数的日志模板
# }
# 
# FORMATTER_KIND = 5  # 默认选择第几个模板

'''


def use_config_form_nb_log_config_module():
    """
    自动读取配置。会优先读取启动脚本的目录的distributed_frame_config.py文件。没有则读取项目根目录下的distributed_frame_config.py
    :return:
    """
    line = sys._getframe().f_back.f_lineno
    file_name = sys._getframe(1).f_code.co_filename
    try:
        m = importlib.import_module('nb_log_config')
        msg = f'nb_log包 读取到\n "{m.__file__}:1" 文件里面的变量作为优先配置了\n'
        # nb_print(msg)
        sys.stdout.write(f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   {msg} \n \033[0m')
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(nb_log_config_default, var_namex, var_valuex)
    except ModuleNotFoundError:
        msg = f'''在你的项目根目录下生成了 \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" 的nb_log包的日志配置文件，快去看看并修改一些自定义配置吧'''
        sys.stdout.write(f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   {msg} \n \033[0m')
        auto_creat_config_file_to_project_root_path()


def auto_creat_config_file_to_project_root_path():
    # print(Path(sys.path[1]).as_posix())
    # print((Path(__file__).parent.parent).absolute().as_posix())
    """
    :return:
    """
    if Path(sys.path[1]).as_posix() in Path(__file__).parent.parent.absolute().as_posix():
        pass
        nb_print('不希望在本项目里面创建')
        return
    """
    如果没设置PYTHONPATH，sys.path会这样，取第一个就会报错
    ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']
    
    ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
    """
    if  '/lib/python' in sys.path[1]  or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
        return   # 当没设置pythonpath时候，也不要在 /lib/python36.zip这样的地方创建配置文件。
    with (Path(sys.path[1]) / Path('nb_log_config.py')).open(mode='w', encoding='utf8') as f:
        f.write(config_file_content)


use_config_form_nb_log_config_module()
