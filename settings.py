# 代理ip的默认最高可用性
MAX_SCORE = 10

# 日志的配置信息
import logging

# 默认的配置
# LOG_LEVEL = logging.INFO  # 默认等级
LOG_LEVEL = logging.DEBUG
LOG_FMT = '%(asctime)s %(filename)s [lines:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
LOG_DATEFMT = '%Y-%M-%D %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件的名字

# 测试代理ip的超时时间
TEST_TIMEOUT = 5

# mongodb数据库的url
MONGO_URL = 'mongodb://127.0.0.1:27017'

# 爬虫的全类名 路径：模块：类名
PROXIES_SPIDERS = [
    'core.proxy_spider.spider_proxy.YqieSpider',
    'core.proxy_spider.spider_proxy.SixsixSpider',
    'core.proxy_spider.spider_proxy.Ip3366Spider',
    'core.proxy_spider.spider_proxy.EightnineSpider',
    'core.proxy_spider.spider_proxy.QiyunSpider',
    'core.proxy_spider.spider_proxy.ProxylistplusSpider',
    'core.proxy_spider.spider_proxy.KuaiSpider'
]

# 运行爬虫每间隔小时执行一次
RUN_SPIDERS_INTERVAL = 1
# 检测代理ip的时间间隔,单位分钟
TEST_PROXIES_INTERVAL = 1
# 检测代理ip的异步数量
TEST_PROXIES_ASYNC_COUNT = 10
# 配置获取代理IP的最大数量，值越小，可用性就高，随机性就差
PROXIES_MAX_COUNT = 10
