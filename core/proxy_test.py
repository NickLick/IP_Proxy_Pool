# 实现代理池检测模块
# 检查代理ip的可用性，保证代理池中的代理ip基本可用
# 导入协程
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_INTERVAL, TEST_PROXIES_ASYNC_COUNT
# import schedule
import time
from utils.log import logger

class ProxyTest(object):
    def __init__(self):
        # 创建操作数据库的对象
        self.mongo_pool = MongoPool()
        # 队列对象
        self.queue = Queue()
        # 协程对象
        self.coroutine_pool = Pool()

    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    # 用于处理检测代理ip的核心逻辑
    def run(self):
        # 从数据库里面获取所有的代理ip
        proxies = self.mongo_pool.find_all()
        # 遍历检测所有的代理ip
        for proxy in proxies:
            # 把代理ip添加到队列中
            self.queue.put(proxy)
        # 通过协程异步执行检测代理
        # 开启多个异步任务，来处理代理ip的检测
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)
        # 让当前线程等待队列完成
        self.queue.join()

    # 检查一个代理ip的可用性
    def __check_one_proxy(self):
        # 从队列中获取proxy，在进行检查
        proxy = self.queue.get()
        logger.info("正在检查代理{}".format(proxy))
        proxy = check_proxy(proxy)
        # 如果不可用，代理分数减一
        if proxy.speed == -1:
            proxy.score -= 1
            logger.info("代理{}检查不可用，分数减一".format(proxy))
            # 代理ip分数0，从数据库删除
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            # 不为0，对该代理ip进行更新
            else:
                self.mongo_pool.update_one(proxy)
        # 如果监测可用，恢复该代理的分数，更新到数据库
        else:
            logger.info("代理{}检查可用，分数恢复".format(proxy))
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        # 调度队列的task_done，判断队列完成
        self.queue.task_done()

    @classmethod
    def start(cls):
        # 类方法
        # 创建类对象 ，执行第一次run
        # 使用schedule模块，每间隔一段时间，执行run
        pt = ProxyTest()
        # pt.run()
        # schedule.every(TEST_PROXIES_INTERVAL).minutes.do(pt.run())
        while True:
            # schedule.run_pending()
            logger.info("开始进行定时检查代理.................")
            pt.run()
            logger.info("检查代理结束，等待%ds进行下一次检查................." % TEST_PROXIES_INTERVAL)
            time.sleep(TEST_PROXIES_INTERVAL)


if __name__ == '__main__':
    ProxyTest.start()
