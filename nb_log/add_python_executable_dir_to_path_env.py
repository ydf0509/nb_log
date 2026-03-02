
import os
import sys

def add_sys_executable_dir_to_path_env():
    """
    动态获取当前Python解释器的绝对路径所处文件夹
    """

    #  #conda虚拟环境需要这样的pywin32在环境变量,linux用户不用管;否则必须先conda activate 虚拟环境,再运行python脚本,但这样太耗时
    # 把当前python解释器所在目录添加到环境变量,则不需要先conda activate 虚拟环境,再运行python脚本
    """
        import nb_log
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\nb_log\__init__.py", line 22, in <module>
    from nb_log import handlers
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\nb_log\handlers.py", line 25, in <module>
    from concurrent_log_handler import ConcurrentRotatingFileHandler  # 需要安装。concurrent-log-handler==0.9.1
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\concurrent_log_handler\__init__.py", line 66, in <module>
    from portalocker import LOCK_EX, lock, unlock
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\portalocker\__init__.py", line 4, in <module>
    from . import portalocker
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\portalocker\portalocker.py", line 11, in <module>
    import win32file
ImportError: DLL load failed while importing win32file: 找不到指定的模块。
    """
    # python_dir = os.path.dirname(sys.executable)
    real_python_executable = os.path.realpath(sys.executable)
    python_dir = os.path.dirname(real_python_executable)
    if os.name == 'nt':
        os.environ['path'] = python_dir + os.pathsep + os.environ['PATH']
    # print(f'{__file__} curernt python executable dir: {python_dir}')

add_sys_executable_dir_to_path_env()


