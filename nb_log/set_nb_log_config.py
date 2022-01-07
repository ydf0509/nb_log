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
from nb_log.monkey_print import stdout_write, stderr_write, is_main_process
from shutil import copyfile



# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring,PyPep8
def nb_print(*args, sep=' ', end='\n', file=None):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args))  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    else:
        # 获取被调用函数在被调用时所处代码行数
        line = sys._getframe().f_back.f_lineno
        # 获取被调用函数所在模块文件名
        file_name = sys._getframe(1).f_code.co_filename
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        if nb_log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
            stdout_write(
                f'\033[0;34m{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   \033[0;37;44m{sep.join(args)}\033[0m{end} \033[0m')  # 36  93 96 94
        else:
            stdout_write(
                f'\033[0;34m{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end} \033[0m')  # 36  93 96 94
        # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')


nb_print(f'当前项目的根目录是：\n {sys.path[1]}')   # 如果获取的项目根目录不正确，请不要在python代码硬编码操作sys.path。pycahrm自动给项目根目录加了PYTHONPATh，如果是shell命令行运行python命令前脚本前先在会话中设置临时环境变量 export PYTHONPATH=项目根目录

def show_nb_log_config():
    nb_print('显示nb_log 包的默认的低优先级的配置参数')
    for var_name in dir(nb_log_config_default):
        nb_print(var_name, getattr(nb_log_config_default, ':', var_name))
    print('\n')


# noinspection PyProtectedMember
def use_config_form_nb_log_config_module():
    """
    自动读取配置。会优先读取启动脚本的目录的distributed_frame_config.py文件。没有则读取项目根目录下的distributed_frame_config.py
    :return:
    """
    line = sys._getframe().f_back.f_lineno
    # noinspection PyProtectedMember
    file_name = sys._getframe(1).f_code.co_filename
    try:
        m = importlib.import_module('nb_log_config')
        importlib.reload(m)  # 这行是防止用户在导入框架之前，写了 from nb_log_config import xx 这种，导致 m.__dict__.items() 不包括所有配置变量了。
        msg = f'nb_log包 读取到\n "{m.__file__}:1" 文件里面的变量作为优先配置了\n'
        # nb_print(msg)
        if is_main_process():
            stdout_write(f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   {msg} \n \033[0m')
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(nb_log_config_default, var_namex, var_valuex)
    except ModuleNotFoundError:
        auto_creat_config_file_to_project_root_path()
        msg = f'''在你的项目根目录下生成了 \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" 的nb_log包的日志配置文件，快去看看并修改一些自定义配置吧'''
        stdout_write(f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"   {msg} \n \033[0m')


def auto_creat_config_file_to_project_root_path():
    # print(Path(sys.path[1]).as_posix())
    # print((Path(__file__).parent.parent).absolute().as_posix())
    """
    :return:
    """
    if Path(sys.path[1]).as_posix() == Path(__file__).parent.parent.absolute().as_posix():
        pass
        nb_print('不希望在本项目 sys.path[1] 里面创建 nb_log_config.py')
        return
    # noinspection PyPep8
    """
        如果没设置PYTHONPATH，sys.path会这样，取第一个就会报错
        ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']
        
        ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
        """
    if '/lib/python' in sys.path[1] or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
        raise EnvironmentError('''如果用pycahrm启动，默认不需要你手动亲自设置PYTHONPATH，如果你是cmd或者shell中直接敲击python xx.py 来运行，
                               报现在这个错误，你现在肯定是没有设置PYTHONPATH环境变量，不要设置永久环境变量，设置临时会话环境变量就行，
                               windows设置  set PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               linux设置    export PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               要是连PYTHONPATH这个知识点都不知道，那就要google 百度去学习PYTHONPATH作用了，非常重要非常好用，
                               不知道PYTHONPATH作用的人，在深层级文件夹作为运行起点导入外层目录的包的时候，如果把深层级文件作为python的执行文件起点，经常需要到处很low的手写 sys.path.insert硬编码，这种方式写代码太low了。
                               知道PYTHONPATH的人无论项目有多少层级的文件夹，无论是多深层级文件夹导入外层文件夹，代码里面永久都不需要出现手动硬编码操纵sys.path.append
                               
                               懂PYTHONPATH 的重要性和妙用见： https://github.com/ydf0509/pythonpathdemo
                               ''')
    # with (Path(sys.path[1]) / Path('nb_log_config.py')).open(mode='w', encoding='utf8') as f:
    #     f.write(config_file_content)
    copyfile(Path(__file__).parent / Path('nb_log_config_default.py'), Path(sys.path[1]) / Path('nb_log_config.py'))


use_config_form_nb_log_config_module()
