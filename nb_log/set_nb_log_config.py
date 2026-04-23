# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/4/11 0011 0:56
"""
Configuration module that uses an override approach.
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
    en_msg = f'The project root directory is:\n {sys.path[1]}'
    sprint(en_msg, only_print_on_main_process=True)


def show_nb_log_config():
    en_msg = 'Show the default low priority configuration parameters of the nb_log package'
    sprint(en_msg)
    for var_name in dir(nb_log_config_default):
        sprint(var_name, getattr(nb_log_config_default, ':', var_name))
    print('\n')


# noinspection PyProtectedMember
def use_config_form_nb_log_config_module():
    """
    Auto-read configuration. Prioritizes nb_log_config.py from the startup script directory,
    then falls back to the project root directory.
    :return:
    """
    try:
        m = importlib.import_module('nb_log_config')
        importlib.reload(m)  # Reload to ensure all config variables are captured, even if user imported specific vars before.

        en_msg1 = f'nb_log has read the configuration variables in the \n "{m.__file__}:1" file as priority configuration\n'
        if _get_show_import_nb_log_config_path():
            sprint(en_msg1, only_print_on_main_process=True)
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(nb_log_config_default, var_namex, var_valuex)
    except ModuleNotFoundError:
        auto_creat_config_file_to_project_root_path()
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
        en_msg1 = f'It is not expected to create the nb_log_config.py file in this project {sys.path[1]}'
        sprint(en_msg1, only_print_on_main_process=True)
        return
    # noinspection PyPep8
    """
        Without PYTHONPATH set, sys.path looks like this, and using the first entry would cause errors
        ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']
        
        ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
        """
    if  nb_log_config_default.judge_has_set_pythonpath() is False:  # Indicates PYTHONPATH is not set
        en_err_msg2 = f'''If you use PyCharm to start the project, PYTHONPATH is set automatically.
                               If you run python directly from cmd or shell and get this error,
                               you need to set the PYTHONPATH environment variable (use a temporary session variable, not a permanent one).
                               Windows: set PYTHONPATH=your_project_root_directory, then run your python command.
                               Linux: export PYTHONPATH=your_project_root_directory, then run your python command.
                               Understanding PYTHONPATH eliminates the need for manual sys.path.insert() hacks.
                               See: https://github.com/ydf0509/pythonpathdemo for more details.
                               '''
        # raise EnvironmentError(en_err_msg2) # Users should set PYTHONPATH
        sprint(f'\033[91m{en_err_msg2}\033[0m', only_print_on_main_process=True)
        return 
    # with (Path(sys.path[1]) / Path('nb_log_config.py')).open(mode='w', encoding='utf8') as f:
    #     f.write(config_file_content)
    copyfile(Path(__file__).parent / Path('nb_log_config_default.py'), Path(sys.path[1]) / Path('nb_log_config.py'))
    en_msg3 = f'''A file has been automatically generated in the {Path(sys.path[1])} directory. Please refresh the folder to view or modify \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" file'''
    sprint(en_msg3)


use_config_form_nb_log_config_module()
