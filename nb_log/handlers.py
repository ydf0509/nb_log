# noinspection PyMissingOrEmptyDocstring
import atexit
import copy
import multiprocessing
import queue
import re
import sys
import os
import threading
import traceback
import socket
import datetime
import json
import time
import typing

from collections import OrderedDict
from pathlib import Path
from queue import Queue, Empty

from threading import Lock, Thread
import requests
import logging
from logging import handlers

# noinspection PyUnresolvedReferences
from logging.handlers import WatchedFileHandler
# noinspection PyPackageRequirements
from nb_filelock import FileLock
from pythonjsonlogger.jsonlogger import JsonFormatter
from nb_log import nb_log_config_default
from nb_log.monkey_print import nb_print
from nb_log.rotate_file_writter import OsFileWritter

very_nb_print = nb_print
os_name = os.name

host_name = socket.gethostname()


# noinspection PyPep8Naming
def formatMessage(self, record: logging.LogRecord):
    # print(record.__dict__)
    if hasattr(record, 'for_segmentation_color'):
        # del record.for_segmentation_color
        # del record.msg
        record.message = ''
    # print(record.__dict__)
    return self._style.format(record)


# logging.Formatter.formatMessage = formatMessage


class ColorHandler(logging.Handler):
    """
    Displays color-coded console logs based on log severity level.
    For best results, use PyCharm's monokai theme: Settings -> Editor -> Color Scheme -> Console Font -> monokai.
    """

    terminator = '\r\n' if os_name == 'nt' else '\n'
    bule = 96 if os_name == 'nt' else 36
    yellow = 93 if os_name == 'nt' else 33

    def __init__(self, stream=None, ):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        logging.Handler.__init__(self)
        if stream is None:
            stream = sys.stdout  # stderr doesn't support colors
        self.stream = stream
        self._display_method = 7 if os_name == 'posix' else 0

    def flush(self):
        """
        Flushes the stream.
        """
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()

    def __build_color_msg_with_backgroud_color000(self, record_level, assist_msg, effective_information_msg):

        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # green
            # print(msg1)
            msg_color = f'\033[0;32m{assist_msg}\033[0m \033[0;37;42m{effective_information_msg}\033[0m'  # green
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # cyan 36    96
            msg_color = f'\033[0;36m{assist_msg}\033[0m \033[0;37;46m{effective_information_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{assist_msg}\033[0m \033[0;37;43m{effective_information_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # magenta
            msg_color = f'\033[0;35m{assist_msg}\033[0m \033[0;37;45m{effective_information_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # red
            msg_color = f'\033[0;31m{assist_msg}\033[0m \033[0;37;41m{effective_information_msg}\033[0m'
        else:
            msg_color = f'{assist_msg}  {effective_information_msg}'
        return msg_color

    @staticmethod
    def __build_color_msg_with_no_backgroud_color000(record_level, assist_msg, effective_information_msg):

        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # green
            # print(msg1)
            msg_color = f'\033[0;32m{assist_msg} {effective_information_msg}\033[0m'  # green
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # cyan 36    96
            msg_color = f'\033[0;36m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # magenta
            msg_color = f'\033[0;35m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # red
            msg_color = f'\033[0;31m{assist_msg} {effective_information_msg}\033[0m'
        else:
            msg_color = f'{assist_msg}  {effective_information_msg}'
        return msg_color

    def __build_color_msg_with_backgroud_color(self, record_level, record_copy: logging.LogRecord, ):
        background_color = ''
        complete_color = ''
        if record_level == 10:
            background_color = f'[0;30;42m'
            complete_color = f'[0;32m'
        elif record_level == 20:
            background_color = f'[0;30;46m'
            complete_color = f'[0;36m'
        elif record_level == 30:
            background_color = f'[0;30;43m'
            complete_color = f'[0;33m'
        elif record_level == 40:
            background_color = f'[0;37;45m'
            complete_color = f'[0;35m'
        elif record_level == 50:
            background_color = f'[0;37;41m'
            complete_color = f'[0;31m'
        record_copy.msg = f'\033{background_color}{record_copy.msg}\033[0m'
        msg_color_without = self.format(record_copy)
        # print(repr(msg_color))
        if isinstance(self.formatter, JsonFormatter) and background_color:  # JSON escapes \033 to \u001b, breaking color display.
            msg_color_without = msg_color_without.replace(rf'\u001b{background_color}', f'\033{background_color}')
            msg_color_without = msg_color_without.replace(r'\u001b[0m', f'\033[0m\033{complete_color}')
        msg_color = f'\033{complete_color}{msg_color_without}\033[0m'
        # print(repr(msg_color))
        return msg_color


    def __build_color_msg_with_backgroud_color3333(self, record_level, record_copy: logging.LogRecord, ):
        background_color = ''
        complete_color = ''
        if record_level == 10:
            background_color = f'[0;30;42m'
            complete_color = f'[0;32m'
        elif record_level == 20:
            background_color = f'[0;30;46m'
            complete_color = f'[0;36m'
        elif record_level == 30:
            background_color = f'[0;30;43m'
            complete_color = f'[0;33m'
        elif record_level == 40:
            background_color = f'[0;37;45m'
            complete_color = f'[0;35m'
        elif record_level == 50:
            background_color = f'[0;37;41m'
            complete_color = f'[0;31m'
        record_copy.msg = f'\033{complete_color}{record_copy.msg}\033[0m'
        msg_color_without = self.format(record_copy)
        # print(repr(msg_color))
        if isinstance(self.formatter, JsonFormatter) and background_color:  # JSON escapes \033 to \u001b, breaking color display.
            msg_color_without = msg_color_without.replace(rf'\u001b{background_color}', f'\033{background_color}')
            msg_color_without = msg_color_without.replace(r'\u001b[0m', f'\033[0m\033{complete_color}')
        # msg_color = f'\033{complete_color}{msg_color_without}\033[0m'
        msg_color = f'\033{background_color}{msg_color_without}\033[0m'
        # print(repr(msg_color))
        return msg_color

    def __build_color_msg_with_no_backgroud_color(self, record_level, record_copy: logging.LogRecord, ):
        complete_msg = self.format(record_copy)
        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # green
            # print(msg1)
            msg_color = f'\033[0;32m{complete_msg}\033[0m'  # green
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # cyan 36    96
            msg_color = f'\033[0;36m{complete_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{complete_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # magenta
            msg_color = f'\033[0;35m{complete_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # red
            msg_color = f'\033[0;31m{complete_msg}\033[0m'
        else:
            msg_color = f'{complete_msg}'
        return msg_color

    def emit(self, record: logging.LogRecord):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        # noinspection PyBroadException
        try:
            # very_nb_print(record)
            # record.message = record.getMessage()
            # effective_information_msg = record.getMessage()  # Can't use msg field directly - some packages add extra format fields
            # record_copy = copy.copy(record)  # Copy to prevent color formatting from affecting other handlers (file, DingTalk, etc.)
            # record_copy.for_segmentation_color = 'color_segmentation_marker'
            # del record_copy.msg
            # assist_msg = self.format(record_copy)
            # print(f'**  {assist_msg}  ** ')
            stream = self.stream
            # print(assist_msg)
            # print(effective_information_msg)
            # record.raw_no_color_msg = record.msg
            if nb_log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
                msg_color = self.__build_color_msg_with_backgroud_color(record.levelno, copy.copy(record))
            else:
                msg_color = self.__build_color_msg_with_no_backgroud_color(record.levelno, copy.copy(record))
            # stream.write(msg_color)
            # stream.write(self.terminator)
            # self.flush()
            stream.write(msg_color + self.terminator)
            # self.flush()
        except Exception as e:
            very_nb_print(e)
            very_nb_print(traceback.format_exc())
            # self.handleError(record)

    @staticmethod
    def __spilt_msg(log_level, msg: str):
        split_text = '- LEVEL -'
        if log_level == logging.DEBUG:
            split_text = '- DEBUG -'
        elif log_level == logging.INFO:
            split_text = '- INFO -'
        elif log_level == logging.WARNING:
            split_text = '- WARNING -'
        elif log_level == 40:
            split_text = '- ERROR -'
        elif log_level == 50:
            split_text = '- CRITICAL -'
        msg_split = msg.split(split_text, maxsplit=1)
        return msg_split[0] + split_text, msg_split[-1]

    def __repr__(self):
        level = logging.getLevelName(self.level)
        name = getattr(self.stream, 'name', '')
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)



class CompatibleSMTPSSLHandler(handlers.SMTPHandler):
    """
    An enhanced SMTPHandler that supports both SMTP and SMTP_SSL, with rate limiting for email sending.
    """

    def __init__(self, mailhost, fromaddr, toaddrs: tuple, subject,
                 credentials=None, secure=None, timeout=5.0, is_use_ssl=True, mail_time_interval=0):
        """

        :param mailhost:
        :param fromaddr:
        :param toaddrs:
        :param subject:
        :param credentials:
        :param secure:
        :param timeout:
        :param is_use_ssl:
        :param mail_time_interval: Min interval between emails in seconds. 0 for no rate limit. 60 means at most one email per minute.
        """
        # noinspection PyCompatibility
        # very_nb_print(credentials)
        # noinspection PyTypeChecker
        super().__init__(mailhost, fromaddr, toaddrs, subject,
                         credentials, secure, timeout)
        self._is_use_ssl = is_use_ssl
        self._current_time = 0
        self._time_interval = 3600 if mail_time_interval < 3600 else mail_time_interval  # Min 60 min interval for bulk emails.
        self._msg_map = dict()  # Maps message content to last send timestamp
        self._lock = Lock()

    def emit0(self, record: logging.LogRecord):
        """
        Deprecated: content-based deduplication approach.
        """
        from threading import Thread
        if sys.getsizeof(self._msg_map) > 10 * 1000 * 1000:
            self._msg_map.clear()
        if record.msg not in self._msg_map or time.time() - self._msg_map[record.msg] > self._time_interval:
            self._msg_map[record.msg] = time.time()
            Thread(target=self.__emit, args=(record,)).start()
        else:
            very_nb_print(f' Email sending too frequent (interval < 60 min), skipping: {record.msg}    ')

    def emit(self, record: logging.LogRecord):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        from threading import Thread
        with self._lock:
            if time.time() - self._current_time > self._time_interval:
                self._current_time = time.time()
                Thread(target=self.__emit, args=(record,)).start()
            else:
                very_nb_print(f' Email sending too frequent (interval < {self._time_interval}s), skipping: {record.msg}     ')

    # noinspection PyUnresolvedReferences
    def __emit(self, record):
        # noinspection PyBroadException
        try:
            import smtplib
            from email.message import EmailMessage
            import email.utils
            t_start = time.time()
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout) if self._is_use_ssl else smtplib.SMTP(
                self.mailhost, port, timeout=self.timeout)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
            # noinspection PyPep8
            very_nb_print(
                f'Email sent to {self.toaddrs} successfully, '
                f'took {round(time.time() - t_start, 2)}s, content: {record.msg}                    \033[0;35m!!! Please check your inbox, it may be in spam\033[0m')
        except Exception as e:
            # self.handleError(record)
            very_nb_print(
                f'[log_manager.py]   {time.strftime("%H:%M:%S", time.localtime())}  \033[0;31m !!!!!! Email sending failed: {e} \033[0m')


class DingTalkHandler(logging.Handler):
    _lock_for_remove_handlers = Lock()

    def __init__(self, ding_talk_token=None, time_interval=60):
        super().__init__()
        self.ding_talk_token = ding_talk_token
        self._ding_talk_url = f'https://oapi.dingtalk.com/robot/send?access_token={ding_talk_token}'
        self._current_time = 0
        self._time_interval = time_interval  # Avoid sending too frequently.
        self._lock = Lock()

    def emit(self, record):
        # from threading import Thread
        with self._lock:
            if time.time() - self._current_time > self._time_interval:
                # very_nb_print(self._current_time)
                self._current_time = time.time()
                self.__emit(record)
                # Thread(target=self.__emit, args=(record,)).start()

            else:
                very_nb_print(f' DingTalk message rate limited (interval < {self._time_interval}s), skipping: {record.msg}    ')

    def __emit(self, record):
        message = self.format(record)
        very_nb_print(message)
        data = {"msgtype": "text", "text": {"content": message, "title": 'Log Alert'}}
        try:
            self._remove_urllib_hanlder()  # Prevents circular logging when requests/urllib3 namespace also has a DingTalk handler attached.
            resp = requests.post(self._ding_talk_url, json=data, timeout=(5, 5))
            very_nb_print(f'DingTalk response: {resp.text}')
        except requests.RequestException as e:
            very_nb_print(f"Failed to send DingTalk message: {e}")

    def __repr__(self):
        level = logging.getLevelName(self.level)
        return '<%s (%s)>' % (self.__class__.__name__, level) + ' dingtalk token is ' + self.ding_talk_token

    @classmethod
    def _remove_urllib_hanlder(cls):
        for name in ['root', 'urllib3', 'requests']:
            cls.__remove_urllib_hanlder_by_name(name)

    @classmethod
    def __remove_urllib_hanlder_by_name(cls, logger_name):
        with cls._lock_for_remove_handlers:
            for index, hdlr in enumerate(logging.getLogger(logger_name).handlers):
                if 'DingTalkHandler' in str(hdlr):
                    logging.getLogger(logger_name).handlers.pop(index)


# noinspection PyPep8Naming
class ConcurrentDayRotatingFileHandlerWin(logging.Handler):
    """
    Multi-process safe time-based rotating file handler.
    The built-in TimedRotatingFileHandler throws errors under multi-process scenarios.
    """
    file_handler_list = []
    has_start_emit_all_file_handler_process_id_set = set()  # Compatible with both Linux and Windows. On Windows each process has independent state; on Linux it's shared.
    __lock_for_rotate = Lock()

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            # print(os.getpid())
            for hr in cls.file_handler_list:
                # very_nb_print(hr.buffer_msgs_queue.qsize())
                # noinspection PyProtectedMember
                hr._write_to_file()
            time.sleep(1)  # Batch write every 1 second for much better performance.

    @classmethod
    def _start_emit_all_file_handler(cls):
        pass
        Thread(target=cls._emit_all_file_handler, daemon=True).start()

    # noinspection PyMissingConstructor
    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = 0

        self.buffer_msgs_queue = queue.Queue()
        atexit.register(self._write_to_file)  # Ensure buffered logs are flushed before program exit.
        self.file_handler_list.append(self)
        if os.getpid() not in self.has_start_emit_all_file_handler_process_id_set:
            self._start_emit_all_file_handler()
            self.__class__.has_start_emit_all_file_handler_process_id_set.add(os.getpid())

    def emit(self, record: logging.LogRecord):
        """
        The emit is already locked by logger.handle(), so no additional lock is needed here.
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)

    def _write_to_file(self):  # Could also override close() for cleanup.
        buffer_msgs = ''
        while True:
            # print(self.buffer_msgs_queue.qsize())
            try:
                msg = self.buffer_msgs_queue.get(block=False)
                buffer_msgs += msg + '\n'
                if len(buffer_msgs) > 1000 * 1000 * 10:
                    pass
                    break
            except queue.Empty:
                break
        if buffer_msgs:
            from nb_filelock import FileLock
            with FileLock(self.file_path / Path(f'_delete_{self.file_name}.lock')):
                time_str = time.strftime('%Y-%m-%d')
                # time_str = time.strftime('%H-%M-%S')  # For testing with second-level rotation.
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                with path_obj.open(mode='a', encoding='utf-8') as f:
                    f.write(buffer_msgs)
                    f.flush()
                if time.time() - self._last_delete_time > 60:
                    self._find_and_delete_files()
                    self._last_delete_time = time.time()

    def _find_and_delete_files(self):
        """
        Determine the files to delete when rolling over.
        Variable naming follows the original CPython logging source code convention.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        # print(result)
        for r in result:
            Path(r).unlink()


# noinspection PyPep8Naming
class ConcurrentDayRotatingFileHandlerLinux(logging.Handler):
    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = time.time()

        time_str = time.strftime('%Y-%m-%d')
        # time_str = time.strftime('%H-%M-%S')  # For testing with second-level rotation.
        new_file_name = self.file_name + '.' + time_str
        path_obj = Path(self.file_path) / Path(new_file_name)
        path_obj.touch(exist_ok=True)
        self.fp = open(path_obj, 'a', encoding='utf-8')
        self.time_str = time_str
        self._lock = multiprocessing.Lock()

    def _get_fp(self):
        with self._lock:
            time_str = time.strftime('%Y-%m-%d')
            # time_str = time.strftime('%H-%M-%S')  # For testing with second-level rotation.
            if time_str != self.time_str:
                try:
                    self.fp.close()
                except Exception as e:
                    print(e)
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                self.fp = open(path_obj, 'a', encoding='utf-8')

    def emit(self, record: logging.LogRecord):
        """
        The emit is already locked by logger.handle(), so no additional lock is needed here.
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.fp.write(msg + '\n')
            self.fp.flush()  # Flush to ensure timely writes. Override close() for cleanup of remaining buffer.
        except Exception as e:
            print(e)
            self.handleError(record)
        if time.time() - self._last_delete_time > 60:
            self._get_fp()
            self._find_and_delete_files()
            self._last_delete_time = time.time()

    def close(self):
        with self._lock:
            try:
                self.fp.flush()
                self.fp.close()
            except Exception as e:
                print(e)

    def _find_and_delete_files(self):
        """
        Determine the files to delete when rolling over.
        Variable naming follows the original CPython logging source code convention.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        # print(result)
        for r in result:
            Path(r).unlink()


# noinspection PyPep8Naming
class _ConcurrentSecondRotatingFileHandlerLinux(logging.Handler):
    """Multi-process safe second-level rotating file handler for testing purposes."""

    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = 0

        time_str = time.strftime('%H-%M-%S')  # Second-level rotation for testing.
        new_file_name = self.file_name + '.' + time_str
        path_obj = Path(self.file_path) / Path(new_file_name)
        path_obj.touch(exist_ok=True)
        self.fp = open(path_obj, 'a', encoding='utf-8')
        self.time_str = time_str
        self._lock = multiprocessing.Lock()

    def _get_fp(self):
        with self._lock:
            time_str = time.strftime('%H-%M-%S')
            # time_str = time.strftime('%H-%M-%S')  # For testing with second-level rotation.
            if time_str != self.time_str:
                try:
                    pass
                    # self.fp.close()
                except Exception as e:
                    print(e)
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                self.fp = open(path_obj, 'a', encoding='utf-8')

    def emit(self, record: logging.LogRecord):
        """
        The emit is already locked by logger.handle(), so no additional lock is needed here.
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            if time.time() - self._last_delete_time > 0.5:
                self._get_fp()
                self._find_and_delete_files()
                self._last_delete_time = time.time()
            self.fp.write(msg + '\n')
        except Exception as e:
            print(e)
            self.handleError(record)

    def _find_and_delete_files(self):
        """
        Determine the files to delete when rolling over.
        Variable naming follows the original CPython logging source code convention.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        # print(result)
        for r in result:
            try:
                Path(r).unlink()
                print(f'Deleted {r}')
            except (PermissionError, FileNotFoundError) as e:
                print(e)


ConcurrentDayRotatingFileHandler = ConcurrentDayRotatingFileHandlerWin if os_name == 'nt' else ConcurrentDayRotatingFileHandlerLinux


# ConcurrentDayRotatingFileHandler = ConcurrentSecondRotatingFileHandlerLinux
#
# print(ConcurrentDayRotatingFileHandler)


class BothDayAndSizeRotatingFileHandler(logging.Handler):
    """
    Custom implementation that rotates log files by both time and size.
    """

    def __init__(self, file_name: typing.Optional[str], log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        super().__init__()
        self.baseFilename = Path(log_path).joinpath(file_name).as_posix()
        self.os_file_writter = OsFileWritter(file_name=file_name, log_path=log_path, max_bytes=max_bytes, back_count=back_count)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.os_file_writter.write_2_file(msg + '\n')

    def __repr__(self):
        level = logging.getLevelName(self.level)
        return '<%s %s (%s)>' % (self.__class__.__name__, self.baseFilename, level)
