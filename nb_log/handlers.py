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
from concurrent_log_handler import ConcurrentRotatingFileHandler  # 需要安装。concurrent-log-handler==0.9.1
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
    根据日志严重级别，显示成五彩控制台日志。
    强烈建议使用pycharm的 monokai主题颜色，这样日志的颜色符合常规的交通信号灯颜色指示，色彩也非常饱和鲜艳。
    设置方式为 打开pycharm的settings -> Editor -> Color Scheme -> Console Font 选择monokai
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
            stream = sys.stdout  # stderr无彩。
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
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{assist_msg}\033[0m \033[0;37;42m{effective_information_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{assist_msg}\033[0m \033[0;37;46m{effective_information_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{assist_msg}\033[0m \033[0;37;43m{effective_information_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{assist_msg}\033[0m \033[0;37;45m{effective_information_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
            msg_color = f'\033[0;31m{assist_msg}\033[0m \033[0;37;41m{effective_information_msg}\033[0m'
        else:
            msg_color = f'{assist_msg}  {effective_information_msg}'
        return msg_color

    @staticmethod
    def __build_color_msg_with_no_backgroud_color000(record_level, assist_msg, effective_information_msg):

        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{assist_msg} {effective_information_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
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
        if isinstance(self.formatter, JsonFormatter) and background_color:  # json会把/033 转义成\u001b,导致颜色显示不出来。
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
        if isinstance(self.formatter, JsonFormatter) and background_color:  # json会把/033 转义成\u001b,导致颜色显示不出来。
            msg_color_without = msg_color_without.replace(rf'\u001b{background_color}', f'\033{background_color}')
            msg_color_without = msg_color_without.replace(r'\u001b[0m', f'\033[0m\033{complete_color}')
        # msg_color = f'\033{complete_color}{msg_color_without}\033[0m'
        msg_color = f'\033{background_color}{msg_color_without}\033[0m'
        # print(repr(msg_color))
        return msg_color

    def __build_color_msg_with_no_backgroud_color(self, record_level, record_copy: logging.LogRecord, ):
        complete_msg = self.format(record_copy)
        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{complete_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{complete_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{complete_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{complete_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
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
            # effective_information_msg = record.getMessage()  # 不能用msg字段，例如有的包的日志格式化还有其他字段
            # record_copy = copy.copy(record)  # copy是因为，不要因为要屏幕彩色日志而影响例如文件日志 叮叮日志等其他handler的格式。
            # record_copy.for_segmentation_color = '彩色分段标志属性而已'
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
        split_text = '- 级别 -'
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


class ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(ConcurrentRotatingFileHandler):
    """
    ConcurrentRotatingFileHandler 解决了多进程下文件切片问题，但频繁操作文件锁，带来程序性能巨大下降。
    反复测试极限日志写入频次，在windows上比不切片的写入性能降低100倍。在linux上比不切片性能降低10倍。多进程切片文件锁在windows使用pywin32，在linux上还是要fcntl实现。
    所以此类使用缓存1秒钟内的日志为一个长字符串再插入，大幅度地降低了文件加锁和解锁的次数，速度比不做多进程安全切片的文件写入速度更快。
    主动触发写入文件。
    """
    file_handler_list = []
    has_start_emit_all_file_handler = False  # 只能在windwos运行正常，windwos是多进程每个进程的变量has_start_emit_all_file_handler是独立的。linux是共享的。

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            for hr in cls.file_handler_list:
                # very_nb_print(hr.buffer_msgs_queue.qsize())
                hr.rollover_and_do_write()
            time.sleep(0.1)

    @classmethod
    def start_emit_all_file_handler(cls):
        pass
        Thread(target=cls._emit_all_file_handler, daemon=True).start()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer_msgs_queue = queue.SimpleQueue()
        atexit.register(self._when_exit)  # 如果程序属于立马就能结束的，需要在程序结束前执行这个钩子，防止不到最后一秒的日志没记录到。
        self.file_handler_list.append(self)
        if not self.has_start_emit_all_file_handler:
            self.__class__.has_start_emit_all_file_handler = True
            self.start_emit_all_file_handler()

    def _when_exit(self):
        pass
        self.rollover_and_do_write()

    def emit(self, record):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)

    def rollover_and_do_write(self, ):
        # very_nb_print(self.buffer_msgs_queue.qsize())
        self._rollover_and_do_write()

    def _rollover_and_do_write(self):
        buffer_msgs = ''
        while True:
            try:
                msg = self.buffer_msgs_queue.get(block=False)
                buffer_msgs += msg + '\n'
                # if len(buffer_msgs) > 1000 * 1000 * 100:
                #     break
            except Empty:
                break
        if buffer_msgs:
            try:
                self._do_lock()
                try:
                    if self.shouldRollover(None):
                        self.doRollover()
                except Exception as e:
                    self._console_log("Unable to do rollover: %s" % (e,), stack=True)
                # very_nb_print(len(self._buffer_msgs))
                self.do_write(buffer_msgs)
            finally:
                self._do_unlock()


class ConcurrentRotatingFileHandlerWithBufferInitiativeLinux00000000(ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos):
    """
    ConcurrentRotatingFileHandler 解决了多进程下文件切片问题，但频繁操作文件锁，带来程序性能巨大下降。
    反复测试极限日志写入频次，在windows上比不切片的写入性能降低100倍。在linux上比不切片性能降低10倍。多进程切片文件锁在windows使用pywin32，在linux上还是要fcntl实现。
    所以此类使用缓存1秒钟内的日志为一个长字符串再插入，大幅度地降低了文件加锁和解锁的次数，速度比不做多进程安全切片的文件写入更快。
    主动触发写入文件。
    """
    file_handler_list = []
    has_start_emit_all_file_handler_process_id_set = set()  # 这个linux和windwos都兼容，windwos是多进程每个进程的变量has_start_emit_all_file_handler是独立的。linux是共享的。
    __lock_for_rotate = Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer_msgs_queue = Queue()
        atexit.register(self._when_exit)  # 如果程序属于立马就能结束的，需要在程序结束前执行这个钩子，防止不到最后一秒的日志没记录到。   有个弊端 at_exit 不能在子进程生效，所以不用这个类
        self.file_handler_list.append(self)
        if os.getpid() not in self.has_start_emit_all_file_handler_process_id_set:
            self.start_emit_all_file_handler()
            self.__class__.has_start_emit_all_file_handler_process_id_set.add(os.getpid())

    def rollover_and_do_write(self, ):
        # very_nb_print(self.buffer_msgs_queue.qsize())
        with self.__lock_for_rotate:
            self._rollover_and_do_write()


ConcurrentRotatingFileHandlerWithBufferInitiativeLinux = ConcurrentRotatingFileHandler


class CompatibleSMTPSSLHandler(handlers.SMTPHandler):
    """
    官方的SMTPHandler不支持SMTP_SSL的邮箱，这个可以两个都支持,并且支持邮件发送频率限制
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
        :param mail_time_interval: 发邮件的时间间隔，可以控制日志邮件的发送频率，为0不进行频率限制控制，如果为60，代表1分钟内最多发送一次邮件
        """
        # noinspection PyCompatibility
        # very_nb_print(credentials)
        # noinspection PyTypeChecker
        super().__init__(mailhost, fromaddr, toaddrs, subject,
                         credentials, secure, timeout)
        self._is_use_ssl = is_use_ssl
        self._current_time = 0
        self._time_interval = 3600 if mail_time_interval < 3600 else mail_time_interval  # 60分钟发一次群发邮件，以后用钉钉代替邮件，邮件频率限制的太死了。
        self._msg_map = dict()  # 是一个内容为键时间为值得映射
        self._lock = Lock()

    def emit0(self, record: logging.LogRecord):
        """
        不用这个判断内容
        """
        from threading import Thread
        if sys.getsizeof(self._msg_map) > 10 * 1000 * 1000:
            self._msg_map.clear()
        if record.msg not in self._msg_map or time.time() - self._msg_map[record.msg] > self._time_interval:
            self._msg_map[record.msg] = time.time()
            # print('发送邮件成功')
            Thread(target=self.__emit, args=(record,)).start()
        else:
            very_nb_print(f' 邮件发送太频繁间隔不足60分钟，此次不发送这个邮件内容： {record.msg}    ')

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
                # very_nb_print(f' 邮件发送太频繁间隔不足60分钟，此次不发送这个邮件内容： {record.msg}     ')
                very_nb_print(f' 邮件发送太频繁间隔不足 {self._time_interval}  秒 ，此次不发送这个邮件内容： {record.msg}     ')

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
                f'发送邮件给 {self.toaddrs} 成功，'
                f'用时{round(time.time() - t_start, 2)} ,发送的内容是--> {record.msg}                    \033[0;35m!!!请去邮箱检查，可能在垃圾邮件中\033[0m')
        except Exception as e:
            # self.handleError(record)
            very_nb_print(
                f'[log_manager.py]   {time.strftime("%H:%M:%S", time.localtime())}  \033[0;31m !!!!!! 邮件发送失败,原因是： {e} \033[0m')


class DingTalkHandler(logging.Handler):
    _lock_for_remove_handlers = Lock()

    def __init__(self, ding_talk_token=None, time_interval=60):
        super().__init__()
        self.ding_talk_token = ding_talk_token
        self._ding_talk_url = f'https://oapi.dingtalk.com/robot/send?access_token={ding_talk_token}'
        self._current_time = 0
        self._time_interval = time_interval  # 最好别频繁发。
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
                very_nb_print(f' 此次离上次发送钉钉消息时间间隔不足 {self._time_interval} 秒，此次不发送这个钉钉内容： {record.msg}    ')

    def __emit(self, record):
        message = self.format(record)
        very_nb_print(message)
        data = {"msgtype": "text", "text": {"content": message, "title": '这里的标题能起作用吗？？'}}
        try:
            self._remove_urllib_hanlder()  # 因为钉钉发送也是使用requests实现的，如果requests调用的urllib3命名空间也加上了钉钉日志，将会造成循环，程序卡住。一般情况是在根日志加了钉钉handler。
            resp = requests.post(self._ding_talk_url, json=data, timeout=(5, 5))
            very_nb_print(f'钉钉返回 ： {resp.text}')
        except requests.RequestException as e:
            very_nb_print(f"发送消息给钉钉机器人失败 {e}")

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
    这个多进程按时间切片安全的。
    官方的 TimedRotatingFileHandler 在多进程下疯狂报错，
    不信的话可以试试官方 TimedRotatingFileHandler 多进程写入文件日志，设置成每秒换一个新的文件写(主要是按天来切割要耽误很长的时间才能观察错误)
    """
    file_handler_list = []
    has_start_emit_all_file_handler_process_id_set = set()  # 这个linux和windwos都兼容，windwos是多进程每个进程的变量has_start_emit_all_file_handler是独立的。linux是共享的。
    __lock_for_rotate = Lock()

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            # print(os.getpid())
            for hr in cls.file_handler_list:
                # very_nb_print(hr.buffer_msgs_queue.qsize())
                # noinspection PyProtectedMember
                hr._write_to_file()
            time.sleep(1)  # 每隔一秒钟批量写入一次，性能好了很多。

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
        atexit.register(self._write_to_file)  # 如果程序属于立马就能结束的，需要在程序结束前执行这个钩子，防止不到最后一秒的日志没记录到。
        self.file_handler_list.append(self)
        if os.getpid() not in self.has_start_emit_all_file_handler_process_id_set:
            self._start_emit_all_file_handler()
            self.__class__.has_start_emit_all_file_handler_process_id_set.add(os.getpid())

    def emit(self, record: logging.LogRecord):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)

    def _write_to_file(self):  # 也可以重写 close方法，来处理末尾。
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
            with FileLock(self.file_path / Path(f'_delete_{self.file_name}.lock')):
                time_str = time.strftime('%Y-%m-%d')
                # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
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
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

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
        # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
        new_file_name = self.file_name + '.' + time_str
        path_obj = Path(self.file_path) / Path(new_file_name)
        path_obj.touch(exist_ok=True)
        self.fp = open(path_obj, 'a', encoding='utf-8')
        self.time_str = time_str
        self._lock = multiprocessing.Lock()

    def _get_fp(self):
        with self._lock:
            time_str = time.strftime('%Y-%m-%d')
            # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
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
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.fp.write(msg + '\n')
            self.fp.flush()  # 需要flush才能及时写入。重写close可以写入程序结束前的缓冲。
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
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

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
    """ 按秒切割的多进程安全文件日志，方便测试验证"""

    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = 0

        time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
        new_file_name = self.file_name + '.' + time_str
        path_obj = Path(self.file_path) / Path(new_file_name)
        path_obj.touch(exist_ok=True)
        self.fp = open(path_obj, 'a', encoding='utf-8')
        self.time_str = time_str
        self._lock = multiprocessing.Lock()

    def _get_fp(self):
        with self._lock:
            time_str = time.strftime('%H-%M-%S')
            # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
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
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
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
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

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
                print(f'删除成功 {r}')
            except (PermissionError, FileNotFoundError) as e:
                print(e)


ConcurrentDayRotatingFileHandler = ConcurrentDayRotatingFileHandlerWin if os_name == 'nt' else ConcurrentDayRotatingFileHandlerLinux


# ConcurrentDayRotatingFileHandler = ConcurrentSecondRotatingFileHandlerLinux
#
# print(ConcurrentDayRotatingFileHandler)


class BothDayAndSizeRotatingFileHandler(logging.Handler):
    """
    自己从头开发的按照时间和大小切割
    """

    def __init__(self, file_name: typing.Optional[str], log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        super().__init__()
        self.os_file_writter = OsFileWritter(file_name=file_name, log_path=log_path, max_bytes=max_bytes, back_count=back_count)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.os_file_writter.write_2_file(msg + '\n')
