# 用于对proxies集合进行数据库的相关操作
# 提供基础的数据库增删改查
from pymongo import MongoClient
from settings import MONGO_URL
from utils.log import logger
from domain import Proxy
import pymongo
import random


class MongoPool(object):
    def __init__(self):
        # 建立数据库连接
        self.client = MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    # 关闭数据库连接
    def __del__(self):
        self.client.close()

    # 实现插入功能,插入一个代理ip
    def insert_one(self, proxy):
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
        else:
            logger.warning("已存在的代理:{},取消插入".format(proxy))

    # 实现修改更新功能 修改修个代理ip
    def update_one(self, proxy):
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    # 实现删除功能,根据代理ip删除一个代理
    def delete_one(self, proxy):
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info("代理:{}分数已归零，从数据库删除".format(proxy))

    # 实现查找功能 查询所有的代理ip的功能
    def find_all(self):
        cursor = self.proxies.find()
        for item in cursor:
            # 删除字典id
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    # 实现查询功能:根据条件进行查询，可以指定查询数量，先分数降序，速度升排序，保证优质代理ip优先
    # conditions：查询条件字典
    # count：限制去除多少个代理ip
    # 返回满足要求的代理ip列表
    def find(self, conditions={}, count=0):
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)
        ])
        # 存储查询处理代理ip的列表
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    # 根据协议类型和要访问的域名，获取代理ip列表
    # protocal 协议
    # domain 域名
    # count 限制获取多个ip
    # nick_type 匿名类型
    # 返回
    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        # 查询条件
        conditions = {'nick_type': nick_type}
        # 根据协议，指定查询条件
        if protocol is None:
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protoc0l'] = {'$in': [1, 2]}
        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}
        return self.find(conditions, count=count)

    # 根据协议类型和要访问的域名，随机返回一个满足要求的代理ip proxy对象
    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        return random.choice(proxy_list)

    # 把指定域名添加到指定IP的disable_domain列表中
    # 如果返回成功，就表示添加成功
    def disable_domain(self, ip, domain):
        # 如果disable_domain字段没有这个域名才添加
        if self.proxies.count_documents({'_id': ip, 'disable_domains': domain}) == 0:
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    proxy = Proxy('202.104.113.35', port='55281')
    mongo.insert_one(proxy)
    # proxy = Proxy('202.104.113.35', port='8888')
    # mongo.update_one(proxy)
    # mongo.delete_one(proxy)

    # for proxy in mongo.find_all():
    #    print(proxy)
    for proxy in mongo.find():
        print(proxy)
