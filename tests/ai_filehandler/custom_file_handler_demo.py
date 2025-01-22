import logging
import os
from pathlib import Path
from typing import Optional, IO, Any
import time
import platform
import signal
import atexit


class FileLock:
    """Cross-platform file locking."""
    
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.is_windows = platform.system() == 'Windows'
        if self.is_windows:
            import msvcrt
            self.msvcrt = msvcrt
        else:
            import fcntl
            self.fcntl = fcntl
    
    def acquire(self, blocking=True):
        if self.is_windows:
            while True:
                try:
                    self.msvcrt.locking(self.file_obj.fileno(), self.msvcrt.LK_NBLCK, 1)
                    return True
                except IOError:
                    if not blocking:
                        return False
                    time.sleep(0.1)
        else:
            try:
                mode = self.fcntl.LOCK_EX if blocking else (self.fcntl.LOCK_EX | self.fcntl.LOCK_NB)
                self.fcntl.flock(self.file_obj.fileno(), mode)
                return True
            except (IOError, OSError):
                return False
    
    def release(self):
        if self.is_windows:
            try:
                self.file_obj.seek(0)
                self.msvcrt.locking(self.file_obj.fileno(), self.msvcrt.LK_UNLCK, 1)
            except (IOError, OSError):
                pass
        else:
            try:
                self.fcntl.flock(self.file_obj.fileno(), self.fcntl.LOCK_UN)
            except (IOError, OSError):
                pass


class CustomRotatingFileHandler(logging.Handler):
    """A process-safe rotating file handler that works on both Windows and Unix."""

    def __init__(self, filename: str, mode='a', encoding='utf-8', max_bytes=1024*1024, 
                 buffer_size=8192, backup_count=1, flush_interval=0.1):
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.max_bytes = max_bytes
        self.buffer_size = buffer_size
        self.backup_count = backup_count
        self.flush_interval = flush_interval
        self.buffer = []
        self._file = None
        self._current_size = 0
        self._last_flush_time = time.time()
        
        # 初始化文件锁
        self._lock_file_path = f"{self.filename}.lock"
        self._lock_file = None
        
        # 确保日志目录存在
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # 注册清理函数
        atexit.register(self._cleanup)

    def _acquire_lock(self):
        """获取文件锁"""
        try:
            self._lock_file = open(self._lock_file_path, 'w')
            
            # 在 Windows 上使用 msvcrt
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self._lock_file.fileno(), msvcrt.LK_NBLCK, 1)
            # 在 Unix/Linux 上使用 fcntl
            else:
                import fcntl
                fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            return True
        except (IOError, OSError):
            if self._lock_file:
                self._lock_file.close()
                self._lock_file = None
            return False

    def _release_lock(self):
        """释放文件锁"""
        if self._lock_file:
            try:
                # 在 Windows 上使用 msvcrt
                if os.name == 'nt':
                    import msvcrt
                    msvcrt.locking(self._lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                # 在 Unix/Linux 上使用 fcntl
                else:
                    import fcntl
                    fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_UN)
            except (IOError, OSError):
                pass
            finally:
                self._lock_file.close()
                self._lock_file = None
                try:
                    os.remove(self._lock_file_path)
                except OSError:
                    pass

    def _open_file(self):
        """Open the current base file with the (original) mode and encoding."""
        try:
            self._file = open(self.filename, mode=self.mode, encoding=self.encoding)
            self._current_size = os.path.getsize(self.filename) if os.path.exists(self.filename) else 0
        except Exception as e:
            print(f"Error opening file: {str(e)}")
            self._file = None
            self._current_size = 0

    def _check_file(self) -> bool:
        """
        Check if the current file handle is valid and points to the right file.
        Returns True if the file is valid, False if it needs to be reopened.
        """
        if self._file is None:
            return False
            
        try:
            # Check if file still exists
            if not os.path.exists(self.filename):
                return False
                
            # Check if file has been renamed (inode changed)
            stat_handle = os.fstat(self._file.fileno())
            stat_name = os.stat(self.filename)
            
            if stat_handle.st_ino != stat_name.st_ino:
                return False
                
            return True
        except Exception:
            return False

    def _signal_handler(self, signum, frame):
        """Handle termination signals by flushing and closing the handler."""
        self.close()
        # Re-raise the signal to allow the program to terminate
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    def _cleanup(self):
        """在程序退出时确保所有日志都被写入"""
        try:
            if hasattr(self, 'buffer') and self.buffer:
                self._flush_buffer()
        finally:
            if self._file:
                try:
                    self._file.close()
                except Exception:
                    pass
                self._file = None

    def emit(self, record):
        try:
            msg = self.format(record)
            self.buffer.append(msg + '\n')
            
            current_time = time.time()
            should_flush = (
                len(self.buffer) >= self.buffer_size or
                (current_time - self._last_flush_time) >= self.flush_interval
            )
            
            if should_flush:
                self._flush_buffer()
                self._last_flush_time = current_time
                
        except Exception:
            self.handleError(record)

    def _flush_buffer(self):
        """Flush the buffer to disk."""
        if not self.buffer:
            return
            
        try:
            buffer_content = ''.join(self.buffer)
            buffer_size = len(buffer_content.encode(self.encoding))
            
            # 确保文件已打开
            if not self._check_file():
                self._open_file()
            
            # 获取当前文件大小    
            self._current_size = os.path.getsize(self.filename) if os.path.exists(self.filename) else 0
                
            if self._current_size + buffer_size > self.max_bytes:
                self.rotate()
                self._current_size = 0  # 重置文件大小计数
                
            # 写入文件
            if self._file is not None:
                self._file.write(buffer_content)
                self._file.flush()
                os.fsync(self._file.fileno())
                self._current_size += buffer_size
                self.buffer = []
                
        except Exception as e:
            print(f"Error in _flush_buffer: {e}")
            self.handleError(None)

    def rotate(self):
        """Rotate the current file in a process-safe way."""
        if not self._acquire_lock():
            return

        try:
            # 首先关闭当前文件
            if self._file:
                self._file.close()
                self._file = None

            try:
                # 从最大的编号开始删除多余的日志文件
                for i in range(self.backup_count + 1, 0, -1):
                    sfn = f"{self.filename}.{i}"
                    if os.path.exists(sfn):
                        try:
                            os.remove(sfn)
                        except OSError:
                            pass

                # 从最后一个备份开始重命名
                for i in range(self.backup_count, 0, -1):
                    sfn = f"{self.filename}.{i-1}" if i > 1 else self.filename
                    dfn = f"{self.filename}.{i}"
                    if os.path.exists(sfn):
                        try:
                            if os.path.exists(dfn):
                                os.remove(dfn)
                            os.rename(sfn, dfn)
                        except OSError as e:
                            print(f"Error rotating file {sfn} to {dfn}: {str(e)}")

            finally:
                # 重新打开文件
                try:
                    self._open_file()
                    self._current_size = 0  # 重置大小计数
                except Exception as e:
                    print(f"Error reopening file: {str(e)}")
                
        finally:
            # 释放锁
            self._release_lock()

    def close(self):
        """Close the file handler and release resources."""
        if getattr(self, '_is_closing', False):
            return
        self._is_closing = True
        
        # Flush any remaining buffered messages
        try:
            self._flush_buffer()
        except Exception:
            pass
            
        if self._file:
            try:
                self._file.close()
            except Exception:
                pass
            self._file = None
            
        if self._lock_file:
            self._release_lock()
            try:
                self._lock_file.close()
            except Exception:
                pass
            try:
                os.remove(self._lock_file_path)
            except OSError:
                pass


def main():
    # Create logger
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"
    )

    # Create and configure file handler
    file_handler = CustomRotatingFileHandler(
        filename="/pythonlogs/test.log",
        max_bytes=1024*10240,  # 1MB
        backup_count=3,
        flush_interval=0.1
    )
    
    # file_handler = logging.FileHandler(filename="/pythonlogs/test.log", mode='a', encoding='utf-8') #  
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    for i in range(100000):
        # 模拟正常的应用程序日志记录
        logger.info("Application started")
        
        # 模拟一些业务操作
        logger.debug("Processing user data")
        try:
            # 模拟一个可能出错的操作
            result = 10 / 0
        except Exception as e:
            logger.error(f"Error occurred during calculation: {str(e)}")
            
        # 模拟一些警告情况
        logger.warning("Database connection pool is running low")
        
        # 模拟一些业务统计信息
        logger.info("Daily statistics: 1000 users logged in, 50000 requests processed")
        
        logger.info("Application shutting down")


if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print(f"Time taken: {t2 - t1} seconds")
