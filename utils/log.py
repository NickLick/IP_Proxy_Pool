import sys
import logging

from settings import *


class Logger(object):
    def __init__(self):
        # 获取一个日志对象
        self._logger = logging.getLogger()
        # 设置format对象 格式
        self.formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
        # 设置文件日志模式
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        # 设置终端日志格式
        self._logger.addHandler(self._get_console_handler())
        # 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    # 返回一个用来输出日志的文件的句柄
    def _get_file_handler(self, filename):
        # 获取一个文件日志handler
        filehandler = logging.FileHandler(filename=filename, encoding="utf-8")
        # 设置日志格式
        filehandler.setFormatter(self.formatter)
        return filehandler

    # 返回一个输出到终端日志的句柄
    def _get_console_handler(self):
        # 获取一个终端日志handler
        consolehandler = logging.StreamHandler(sys.stdout)
        consolehandler.setFormatter(self.formatter)
        return consolehandler

    @property
    def logger(self):
        return self._logger


logger = Logger().logger

if __name__ == '__main__':
    logger.debug("debug")
    logger.info("info")
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
