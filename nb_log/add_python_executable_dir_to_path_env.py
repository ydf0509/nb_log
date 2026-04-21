
import os
import sys

def add_sys_executable_dir_to_path_env():
    """
    Dynamically add the current Python interpreter's directory to PATH.
    This enables conda virtual environments to find pywin32 DLLs without requiring 'conda activate' first.
    """
    """
        import nb_log
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\nb_log\__init__.py", line 22, in <module>
    from nb_log import handlers
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\nb_log\handlers.py", line 25, in <module>
    from concurrent_log_handler import ConcurrentRotatingFileHandler  # requires: concurrent-log-handler
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\concurrent_log_handler\__init__.py", line 66, in <module>
    from portalocker import LOCK_EX, lock, unlock
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\portalocker\__init__.py", line 4, in <module>
    from . import portalocker
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\portalocker\portalocker.py", line 11, in <module>
    import win32file
ImportError: DLL load failed while importing win32file: The specified module could not be found.
    """
    # python_dir = os.path.dirname(sys.executable)
    real_python_executable = os.path.realpath(sys.executable)
    python_dir = os.path.dirname(real_python_executable)
    r"""
    All of these need to be added to PATH:
    D:\ProgramData\Miniconda3
    D:\ProgramData\Miniconda3\Library\mingw-w64\bin
    D:\ProgramData\Miniconda3\Library\usr\bin
    D:\ProgramData\Miniconda3\Library\bin
    D:\ProgramData\Miniconda3\bin
    """
    if os.name == 'nt':
        os.environ['path'] = python_dir + os.pathsep + os.environ['PATH']
        os.environ['path'] = fr'{python_dir}\Library\mingw-w64\bin' + os.pathsep + os.environ['PATH']
        os.environ['path'] = fr'{python_dir}\Library\usr\bin' + os.pathsep + os.environ['PATH']
        os.environ['path'] = fr'{python_dir}\Library\bin' + os.pathsep + os.environ['PATH']
        os.environ['path'] = fr'{python_dir}\bin' + os.pathsep + os.environ['PATH']
        
    # print(f'{__file__} curernt python executable dir: {python_dir}')

add_sys_executable_dir_to_path_env()


