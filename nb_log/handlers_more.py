# noinspection PyMissingOrEmptyDocstring

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
# noinspection PyPackageRequirements
from kafka import KafkaProducer
# from elasticsearch import Elasticsearch, helpers  # 性能导入时间消耗2秒,实例化时候再导入。
from threading import Lock, Thread
import pymongo

import logging

from logging.handlers import WatchedFileHandler

from nb_log.monkey_print import nb_print

very_nb_print = nb_print
os_name = os.name

host_name = socket.gethostname()


class MongoHandler(logging.Handler):
    """
    一个mongodb的log handler,支持日志按loggername创建不同的集合写入mongodb中
    """

    # msg_pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+) - (\S*?) - (\S*?) - (\d+) - (\S*?) - ([\s\S]*)')

    def __init__(self, mongo_url, mongo_database='logs'):
        """
        :param mongo_url:  mongo连接
        :param mongo_database: 保存日志的数据库，默认使用logs数据库
        """
        logging.Handler.__init__(self)
        mongo_client = pymongo.MongoClient(mongo_url)
        self.mongo_db = mongo_client.get_database(mongo_database)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            """以下使用解析日志模板的方式提取出字段"""
            # msg = self.format(record)
            # logging.LogRecord
            # msg_match = self.msg_pattern.search(msg)
            # log_info_dict = {'time': msg_match.group(1),
            #                  'name': msg_match.group(2),
            #                  'file_name': msg_match.group(3),
            #                  'line_no': msg_match.group(4),
            #                  'log_level': msg_match.group(5),
            #                  'detail_msg': msg_match.group(6),
            #                  }
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            log_info_dict['line_no'] = record.lineno
            log_info_dict['log_level'] = level_str
            log_info_dict['detail_msg'] = record.msg
            col = self.mongo_db.get_collection(record.name)
            col.insert_one(log_info_dict)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class KafkaHandler(logging.Handler):
    """
    日志批量写入kafka中。
    """
    ES_INTERVAL_SECONDS = 0.5

    host_name = host_name
    host_process = f'{host_name} -- {os.getpid()}'

    script_name = sys.argv[0].split('/')[-1]

    task_queue = Queue()
    last_es_op_time = time.time()
    has_start_do_bulk_op = False
    has_start_check_size_and_clear = False

    kafka_producer = None
    es_index_prefix = 'pylog-'

    def __init__(self, bootstrap_servers, **configs):
        """
        :param elastic_hosts:  es的ip地址，数组类型
        :param elastic_port：  es端口
        :param index_prefix: index名字前缀。
        """
        logging.Handler.__init__(self)
        if not self.__class__.kafka_producer:
            very_nb_print('实例化kafka producer')
            self.__class__.kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, **configs)

        t = Thread(target=self._do_bulk_op)
        t.setDaemon(True)
        t.start()

    @classmethod
    def __add_task_to_bulk(cls, task):
        cls.task_queue.put(task)

    # noinspection PyUnresolvedReferences
    @classmethod
    def __clear_bulk_task(cls):
        cls.task_queue.queue.clear()

    @classmethod
    def _check_size_and_clear(cls):
        """
        如果是外网传输日志到测试环境风险很大，测试环境网络经常打满，传输不了会造成日志队列堆积，会造成内存泄漏，所以需要清理。
        :return:
        """
        if cls.has_start_check_size_and_clear:
            return
        cls.has_start_check_size_and_clear = True

        def __check_size_and_clear():
            while 1:
                size = cls.task_queue.qsize()
                if size > 1000:
                    very_nb_print(f'kafka防止意外日志积累太多了,达到 {size} 个，为防止内存泄漏，清除队列')
                    cls.__clear_bulk_task()
                time.sleep(0.1)

        t = Thread(target=__check_size_and_clear)
        t.setDaemon(True)
        t.start()

    @classmethod
    def _do_bulk_op(cls):
        if cls.has_start_do_bulk_op:
            return

        cls.has_start_do_bulk_op = True
        # very_nb_print(cls.kafka_producer)
        while 1:
            try:
                # noinspection PyUnresolvedReferences
                tasks = list(cls.task_queue.queue)
                cls.__clear_bulk_task()
                for task in tasks:
                    topic = (cls.es_index_prefix + task['name']).replace('.', '').replace('_', '').replace('-', '')
                    # very_nb_print(topic)
                    cls.kafka_producer.send(topic, json.dumps(task).encode())
                cls.last_es_op_time = time.time()
            except Exception as e:
                very_nb_print(e)
            finally:
                time.sleep(cls.ES_INTERVAL_SECONDS)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['@timestamp'] = datetime.datetime.utcfromtimestamp(record.created).isoformat()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['host'] = self.host_name
            log_info_dict['host_process'] = self.host_process
            # log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            # log_info_dict['line_no'] = record.lineno
            log_info_dict['log_place'] = f'{record.pathname}:{record.lineno}'
            log_info_dict['log_level'] = level_str
            log_info_dict['msg'] = str(record.msg)
            log_info_dict['script'] = self.script_name
            log_info_dict['es_index'] = f'{self.es_index_prefix}{record.name.lower()}'
            self.__add_task_to_bulk(log_info_dict)

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class ElasticHandler000(logging.Handler):
    """
    日志批量写入es中。
    """
    ES_INTERVAL_SECONDS = 2
    host_name = host_name

    def __init__(self, elastic_hosts: list, elastic_port, index_prefix='pylog-'):
        """
        :param elastic_hosts:  es的ip地址，数组类型
        :param elastic_port：  es端口
        :param index_prefix: index名字前缀。
        """
        from elasticsearch import Elasticsearch, helpers
        self._helpers = helpers
        logging.Handler.__init__(self)
        self._es_client = Elasticsearch(elastic_hosts, port=elastic_port)
        self._index_prefix = index_prefix
        self._task_list = []
        self._task_queue = Queue()
        self._last_es_op_time = time.time()
        t = Thread(target=self._do_bulk_op)
        t.setDaemon(True)
        t.start()

    def __add_task_to_bulk(self, task):
        self._task_queue.put(task)

    def __clear_bulk_task(self):
        # noinspection PyUnresolvedReferences
        self._task_queue.queue.clear()

    def _do_bulk_op(self):
        while 1:
            try:
                if self._task_queue.qsize() > 10000:
                    very_nb_print('防止意外日志积累太多了，不插入es了。')
                    self.__clear_bulk_task()
                    return
                # noinspection PyUnresolvedReferences
                tasks = list(self._task_queue.queue)
                self.__clear_bulk_task()
                self._helpers.bulk(self._es_client, tasks)

                self._last_es_op_time = time.time()
            except Exception as e:
                very_nb_print(e)
            finally:
                time.sleep(1)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['@timestamp'] = datetime.datetime.utcfromtimestamp(record.created).isoformat()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['host'] = self.host_name
            log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            log_info_dict['line_no'] = record.lineno
            log_info_dict['log_level'] = level_str
            log_info_dict['msg'] = str(record.msg)
            self.__add_task_to_bulk({
                "_index": f'{self._index_prefix}{record.name.lower()}',
                # "_type": '_doc',  # elastic 7 服务端之后不要传递 type了.
                "_source": log_info_dict
            })

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


# noinspection PyUnresolvedReferences
class ElasticHandler(logging.Handler):
    """
    日志批量写入es中。
    """
    ES_INTERVAL_SECONDS = 0.5

    host_name = host_name
    host_process = f'{host_name} -- {os.getpid()}'

    script_name = sys.argv[0]

    task_queue = Queue()
    last_es_op_time = time.time()
    has_start_do_bulk_op = False

    def __init__(self, elastic_hosts: list, elastic_port, index_prefix='pylog-'):
        """
        :param elastic_hosts:  es的ip地址，数组类型
        :param elastic_port：  es端口
        :param index_prefix: index名字前缀。
        """
        logging.Handler.__init__(self)
        from elasticsearch import Elasticsearch, helpers
        self._helpers = helpers
        self._es_client = Elasticsearch(elastic_hosts, )
        self._index_prefix = index_prefix
        t = Thread(target=self._do_bulk_op)
        t.setDaemon(True)
        t.start()

    @classmethod
    def __add_task_to_bulk(cls, task):
        cls.task_queue.put(task)

    # noinspection PyUnresolvedReferences
    @classmethod
    def __clear_bulk_task(cls):
        cls.task_queue.queue.clear()

    def _do_bulk_op(self):
        if self.__class__.has_start_do_bulk_op:
            return
        self.__class__.has_start_do_bulk_op = True
        while 1:
            try:
                if self.__class__.task_queue.qsize() > 10000:
                    very_nb_print('防止意外日志积累太多了，不插入es了。')
                    self.__clear_bulk_task()
                    return
                tasks = list(self.__class__.task_queue.queue)
                self.__clear_bulk_task()
                self._helpers.bulk(self._es_client, tasks)
                self.__class__.last_es_op_time = time.time()
            except Exception as e:
                very_nb_print(e)
            finally:
                time.sleep(self.ES_INTERVAL_SECONDS)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['@timestamp'] = datetime.datetime.utcfromtimestamp(record.created).isoformat()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['host'] = self.host_name
            log_info_dict['host_process'] = self.host_process
            log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            log_info_dict['line_no'] = record.lineno
            log_info_dict['log_level'] = level_str
            log_info_dict['msg'] = str(record.msg)
            log_info_dict['script'] = self.script_name
            self.__add_task_to_bulk({
                "_index": f'{self._index_prefix}{record.name.lower()}',
                # "_type": f'_doc',    # es7 服务端之后不支持_type设置
                "_source": log_info_dict
            })

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
