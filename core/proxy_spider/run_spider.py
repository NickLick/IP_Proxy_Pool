# 爬虫运行模块
# 导入协程
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import importlib
from core.proxy_spider.spider_proxy import *
from settings import PROXIES_SPIDERS, RUN_SPIDERS_INTERVAL
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
# import schedule
import time


class RunSpider(object):
    def __init__(self):
        # 创建mongopool对象
        self.mongo_pool = MongoPool()
        # 创建协程对象
        self.croutine_pool = Pool()

    # 根据配置文件信息，获取爬虫对象
    def get_spider_from_setting(self):
        # 遍历配置文件爬虫信息，获取每个爬虫全类名
        for full_class_name in PROXIES_SPIDERS:
            # 获取模块名，类名
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            # 根据模块名导入模块
            module = importlib.import_module(module_name)
            # 根据类名，从模块中获取类
            cls = getattr(module, class_name)
            # 创建爬虫对象
            one_spider = cls()
            yield one_spider

    # 一个爬虫任务
    def __execute_spider_task(self, one_spider):
        try:
            # 遍历爬虫对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取代理ip
            for proxy in one_spider.get_proxies():
                print(proxy)
                # 检验代理ip可用性
                proxy = check_proxy(proxy)
                # 如果可用，写入数据库
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as ex:
            logger.exception(ex)

    # 遍历爬虫对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取代理ip
    # 检测代理ip（代理ip检测模块）
    # 如果可用，写入数据库（数据库模块）、
    # 处理异常，防止一个爬虫内部出错，影响其他爬虫
    # 使用异步来执行每一个爬虫任务，提高抓取代理ip效率
    def run(self):
        # all_spiders = self.get_spider_from_setting
        # print(all_spiders)
        all_spiders = [SixsixSpider(), YqieSpider(), Ip3366Spider(), KuaiSpider(), ProxylistplusSpider(), QiyunSpider(),
                       EightnineSpider()]
        for one_spider in all_spiders:
            # 使用异步来执行每一个爬虫任务，提高抓取代理ip效率
            self.croutine_pool.apply_async(self.__execute_spider_task, args=(one_spider,))
        # 调用协程的join方法，让当前线程等待协程完成
        self.croutine_pool.join()

    @classmethod
    def start(cls):
        # 类方法
        # 创建类对象 ，执行第一次run
        # 使用schedule模块，每间隔一段时间，执行run
        rs = RunSpider()
        # rs.run()
        # schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run())
        while True:
            rs.run()
            time.sleep(RUN_SPIDERS_INTERVAL*3600)


if __name__ == '__main__':
    RunSpider.start()
