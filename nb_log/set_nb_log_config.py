# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/4/11 0011 0:56
"""

使用覆盖的方式，做配置。
"""
import sys
import importlib
from pathlib import Path
from nb_log import nb_log_config_default
from nb_log.simple_print import sprint
from shutil import copyfile


def _get_show_import_nb_log_config_path():
    try:
        import nb_log_config
        return nb_log_config.SHOW_IMPORT_NB_LOG_CONFIG_PATH
    except Exception as e:
        return True


if _get_show_import_nb_log_config_path():
    cn_msg = f'当前项目的根目录是：\n {sys.path[1]}'
    en_msg = f'The project root directory is:\n {sys.path[1]}'
    sprint(en_msg, only_print_on_main_process=True)  # 如果获取的项目根目录不正确，请不要在python代码硬编码操作sys.path。pycahrm自动给项目根目录加了PYTHONPATh，如果是shell命令行运行python命令前脚本前先在会话中设置临时环境变量 export PYTHONPATH=项目根目录


def show_nb_log_config():
    cn_msg = '显示nb_log 包的默认的低优先级的配置参数'
    en_msg = 'Show the default low priority configuration parameters of the nb_log package'
    sprint(en_msg)
    for var_name in dir(nb_log_config_default):
        sprint(var_name, getattr(nb_log_config_default, ':', var_name))
    print('\n')


# noinspection PyProtectedMember
def use_config_form_nb_log_config_module():
    """
    自动读取配置。会优先读取启动脚本的目录的distributed_frame_config.py文件。没有则读取项目根目录下的distributed_frame_config.py
    :return:
    """
    try:
        m = importlib.import_module('nb_log_config')
        importlib.reload(m)  # 这行是防止用户在导入框架之前，写了 from nb_log_config import xx 这种，导致 m.__dict__.items() 不包括所有配置变量了。

        cn_msg1 = f'nb_log包 读取到\n "{m.__file__}:1" 文件里面的变量作为优先配置了\n'
        en_msg1 = f'nb_log has read the configuration variables in the \n "{m.__file__}:1" file as priority configuration\n'
        # nb_print(msg)
        if _get_show_import_nb_log_config_path():
            sprint(en_msg1, only_print_on_main_process=True)
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(nb_log_config_default, var_namex, var_valuex)
    except ModuleNotFoundError:
        auto_creat_config_file_to_project_root_path()
        cn_msg2 = f'''在你的项目根目录下生成了 \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" 的nb_log包的日志配置文件，快去看看并修改一些自定义配置吧'''
        en_msg2 = f'nb_log has created the configuration file \n "{Path(sys.path[1]) / Path("nb_log_config.py")}:1" in the project root directory.\n Please check and modify some custom configurations.'
        sprint(en_msg2, only_print_on_main_process=True)


def auto_creat_config_file_to_project_root_path():
    # print(Path(sys.path[1]).as_posix())
    # print((Path(__file__).parent.parent).absolute().as_posix())
    """
    :return:
    """
    if Path(sys.path[1]).as_posix() == Path(__file__).parent.parent.absolute().as_posix():
        pass
        cn_msg1 = f'不希望在本项目 {sys.path[1]} 里面创建 nb_log_config.py'
        en_msg1 = f'It is not expected to create the nb_log_config.py file in this project {sys.path[1]}'
        sprint(en_msg1, only_print_on_main_process=True)
        return
    # noinspection PyPep8
    """
        如果没设置PYTHONPATH，sys.path会这样，取第一个就会报错
        ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']
        
        ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
        """
    if '/lib/python' in sys.path[1] or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
        cn_err_msg2 = '''如果用pycahrm启动，默认不需要你手动亲自设置PYTHONPATH，如果你是cmd或者shell中直接敲击python xx.py 来运行，
                               报现在这个错误，你现在肯定是没有设置PYTHONPATH环境变量，不要设置永久环境变量，设置临时会话环境变量就行，
                               windows设置  set PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               linux设置    export PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               要是连PYTHONPATH这个知识点都不知道，那就要google 百度去学习PYTHONPATH作用了，非常重要非常好用，
                               不知道PYTHONPATH作用的人，在深层级文件夹作为运行起点导入外层目录的包的时候，如果把深层级文件作为python的执行文件起点，经常需要到处很low的手写 sys.path.insert硬编码，这种方式写代码太low了。
                               知道PYTHONPATH的人无论项目有多少层级的文件夹，无论是多深层级文件夹导入外层文件夹，代码里面永久都不需要出现手动硬编码操纵sys.path.append
                               
                               懂PYTHONPATH 的重要性和妙用见： https://github.com/ydf0509/pythonpathdemo
                               '''
        en_err_msg2 = f'''If you use pycahrm to start the project, you do not need to manually set the PYTHONPATH environment variable by default.
                               If you run the project directly in the cmd or shell, you will get the current error.
                               You must not set the PYTHONPATH environment variable permanently, but set it temporarily in the session environment variable.
                               Windows setting: set PYTHONPATH=your current python project root directory, then run your python command.
                               Linux setting: export PYTHONPATH=your current python project root directory, then run your python command.
                               If you do not know the PYTHONPATH concept, you should google or baidu to learn about its importance and usage.
                               If you do not know the PYTHONPATH concept, you will often need to write very low-level code to manually manipulate sys.path.append.
                               Understanding the importance and usage of PYTHONPATH is very important and useful.
                               See: https://github.com/ydf0509/pythonpathdemo for more details.
                               '''
        raise EnvironmentError(en_err_msg2)
    # with (Path(sys.path[1]) / Path('nb_log_config.py')).open(mode='w', encoding='utf8') as f:
    #     f.write(config_file_content)
    copyfile(Path(__file__).parent / Path('nb_log_config_default.py'), Path(sys.path[1]) / Path('nb_log_config.py'))
    cn_msg3 = f'''在  {Path(sys.path[1])} 目录下自动生成了一个文件， 请刷新文件夹查看或修改 \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" 文件'''
    en_msg3 = f'''A file has been automatically generated in the {Path(sys.path[1])} directory. Please refresh the folder to view or modify \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" file'''
    sprint(en_msg3)


use_config_form_nb_log_config_module()
