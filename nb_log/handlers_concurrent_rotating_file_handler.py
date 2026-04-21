from concurrent_log_handler import ConcurrentRotatingFileHandler  # requires: concurrent-log-handler
import time
from threading import Thread
import atexit
import queue
from queue import Empty, SimpleQueue

class ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(ConcurrentRotatingFileHandler):
    """
    ConcurrentRotatingFileHandler solves multi-process file rotation but frequent file locking causes significant performance degradation.
    In stress tests: 100x slower on Windows and 10x slower on Linux compared to non-rotating writes.
    This class buffers log messages within a 1-second window and writes them as a single batch,
    drastically reducing lock/unlock operations for better-than-non-rotating performance.
    """
    file_handler_list = []
    has_start_emit_all_file_handler = False  # Only works correctly on Windows where each process has independent state. On Linux the variable is shared.

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
        atexit.register(self._when_exit)  # Ensure buffered logs are flushed before program exit.
        self.file_handler_list.append(self)
        if not self.has_start_emit_all_file_handler:
            self.__class__.has_start_emit_all_file_handler = True
            self.start_emit_all_file_handler()

    def _when_exit(self):
        pass
        self.rollover_and_do_write()

    def emit(self, record):
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





ConcurrentRotatingFileHandlerWithBufferInitiativeLinux = ConcurrentRotatingFileHandler

