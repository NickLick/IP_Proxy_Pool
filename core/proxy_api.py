# 为爬虫提取高可用的代理ip的服务接口
from flask import Flask
from flask import request
import json
from db.mongo_pool import MongoPool
from utils.settings import PROXIES_MAX_COUNT


class ProxyApi(object):
    def __init__(self):
        # 初始化flaskweb服务
        self.app = Flask(__name__)
        # 创建mongopool
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            # 实现根据协议类型和域名，提供随机的获取高可用代理ip的服务
            # 可以通过protocol和domain参数对ip进行过滤
            # protocol：当前请求的协议类型
            # domain：当前请求域名
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=PROXIES_MAX_COUNT)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

        # 随机获取多个代理IP
        @self.app.route('/proxies')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            # proxies现在是一个Proxy对象列表，不能进行json序列化
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=PROXIES_MAX_COUNT)
            # 转换为字典列表
            proxies = [proxy.__dict__ for proxy in proxies]
            return json.dumps(proxies)

        # 请求禁用指定域名
        @self.app.route('/disable_domain')
        def disable_domain():
            ip = request.args.get('ip')
            domain = request.args.get('domain')
            if ip is None:
                return '请提供ip参数'
            if domain is None:
                return '请提供domain参数'
            self.mongo_pool.disable_domain(ip, domain)
            return "{}禁用域名{}成功".format(ip, domain)

    # 启动flask的web服务
    def run(self):
        self.app.run('127.0.0.1', port=8888)

    # 提供启动方法，统一入口
    @classmethod
    def start(cls):
        proxy_api = cls()
        proxy_api.run()


if __name__ == '__main__':
    ProxyApi.start()
