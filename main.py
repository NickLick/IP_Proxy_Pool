# 统一的入口
from multiprocessing import Process
from core.run_spider import RunSpider
from core.proxy_test import ProxyTest
from core.proxy_api import ProxyApi


def run():
    # 存储要启动的进程列表
    process_list = [Process(target=RunSpider.start), Process(target=ProxyTest.start), Process(target=ProxyApi.start)]
    for process in process_list:
        process.daemon = True
        process.start()
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
