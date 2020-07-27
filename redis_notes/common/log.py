#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os
import sys
import time
import random
import string


class CLog(object):
    """ Log wrapper
    """

    LEVEL_MAP = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG
    }

    INSTANCE = None
    LOG_SEQ = 'log_seq'

    @staticmethod
    def instance():
        if CLog.INSTANCE is None:
            CLog.INSTANCE = CLog()

        return CLog.INSTANCE

    @staticmethod
    def get_log_prefix(b_global):
        """ 根据调用关系取得日志产生所有文件名、函数名和行号，由此生成日志消息前缀 """
        if b_global:
            f = sys._getframe().f_back.f_back.f_back.f_back
        else:
            f = sys._getframe().f_back.f_back.f_back
        result = '[%s] [%s] [%d]' % (os.path.basename(f.f_code.co_filename),
                                     f.f_code.co_name, f.f_lineno)
        return result

    @staticmethod
    def get_real_msg(msg, b_global):
        return ('%s[%s]<%s>' % (CLog.get_log_prefix(b_global),
                                CLog.LOG_SEQ, msg))

    @staticmethod
    def random_str(random_length):
        ret_str = ''.join(random.sample(string.ascii_letters + string.digits,
                                        random_length))
        return ret_str

    def __init__(self):
        self._proj = ''
        self._log_dir = None
        self._log_prefix = None
        self._log_level = 4
        self._last_log_name = None
        self._logger = None
        self._b_stream_init = False
        self._last_file_handle = None

    def init(self, proj, log_dir, log_prefix, log_level):
        self._proj = proj
        if log_dir[-1] != '/':
            self._log_dir = log_dir + '/'
        else:
            self._log_dir = log_dir
        self._log_prefix = log_prefix
        if log_level < 0:
            log_level = 0
        elif log_level > 4:
            log_level = 4
        self._log_level = log_level

        CLog.LOG_SEQ = CLog.random_str(8)
        if not os.access(self._log_dir, os.F_OK):
            try:
                os.mkdir(self._log_dir)
            except OSError:
                return -1
        return 0

    def check_log_name(self):
        if self._log_dir is None or self._log_prefix is None:
            return (True, None)
        log_name_arr = ([self._log_dir, self._log_prefix, '_',
                         time.strftime('%Y%m%d'), '.log'])
        log_name = ''.join(log_name_arr)
        if self._last_log_name != log_name or not os.path.exists(log_name):
            return (False, log_name)
        else:
            return (True, log_name)

    def init_logger(self):
        self._logger = logging.getLogger(self._proj)
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s][%(process)d][%(levelname)s]%(message)s')
        if not self._b_stream_init:
            stream_handler = logging.StreamHandler(sys.stderr)
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.DEBUG)
            self._logger.addHandler(stream_handler)
            self._b_stream_init = True
        ret = self.check_log_name()
        if ret[0]:
            return 0
        try:
            log_file_handler = logging.FileHandler(ret[1])
            log_file_handler.setFormatter(formatter)
            log_file_handler.setLevel(CLog.LEVEL_MAP[self._log_level])
            self._logger.addHandler(log_file_handler)
            if self._last_file_handle is not None:
                self._logger.removeHandler(self._last_file_handle)
                self._last_file_handle.close()
            self._last_file_handle = log_file_handler
            self._last_log_name = ret[1]
        except:
            pass
        return 0

    def log_debug(self, msg, b_global=False):
        self.init_logger()
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        self._logger.debug(CLog.get_real_msg(msg, b_global))

    def log_info(self, msg, b_global=False):
        self.init_logger()
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        self._logger.info(CLog.get_real_msg(msg, b_global))

    def log_warning(self, msg, b_global=False):
        self.init_logger()
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        self._logger.warning(CLog.get_real_msg(msg, b_global))

    def log_error(self, msg, b_global=False):
        self.init_logger()
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        self._logger.error(CLog.get_real_msg(msg, b_global))

    def log_critical(self, msg, b_global=False):
        self.init_logger()
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        self._logger.critical(CLog.get_real_msg(msg, b_global))


def log_no_stderr():
    CLog.instance()._b_stream_init = True


def log_init(proj, log_dir, log_prefix, log_level=4):
    return CLog.instance().init(proj, log_dir, log_prefix, log_level)


def log_debug(msg):
    CLog.instance().log_debug(msg, True)


def log_info(msg):
    CLog.instance().log_info(msg, True)


def log_warning(msg):
    CLog.instance().log_warning(msg, True)


def log_error(msg):
    CLog.instance().log_error(msg, True)


def log_critical(msg):
    CLog.instance().log_critical(msg, True)

if __name__ == '__main__':
    log_init('test', '../log', 'test')
    log_debug('1111')
    time.sleep(1)
    log_debug('222')
