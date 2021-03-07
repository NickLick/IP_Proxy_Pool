# 实现指定不同URL列表，分组的XPATH和详细的XPATH，从不同页面上提取代理ip，端口号和区域的通用爬虫
import requests
from utils.http import get_request_headers
from lxml import etree
from domain import Proxy
from settings import TEST_TIMEOUT


# from utils.log import logger


class BaseSpider(object):
    # 代理ip网址的url列表
    urls = []
    # 分组xpath，获取包含代理ip信息标签列表的xpath
    group_xpath = ''
    # 组内xpath，获取代理ip详细信息的xpath，格式为（"ip":"xxx","port":"xxx","area":"xxx")
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    # 根据url发送请求，获取页面数据
    def get_page_from_url(self, url):
        # logger.info('begin get page')
        response = requests.get(url, headers=get_request_headers(), timeout=TEST_TIMEOUT)
        # logger.info('success get page')
        return response.content
        # return response.content.decode()

    # 如果列表中有元素就返回第一个，否则空字符串
    def get_first_from_list(self, lists):
        return lists[0] if len(lists) != 0 else ''

    # 解析页面，提取数据，封装为proxy对象
    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        # 获取包含代理ip信息的标签列表
        trs = element.xpath(self.group_xpath)
        # 遍历trs，获取代理ip相关ip信息
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            yield proxy

    # 对外提供一个获取代理ip的方法
    def get_proxies(self):
        # 遍历url列表，获取url
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies


if __name__ == '__main__':
    config = {
        'urls': ['https://www.kuaidaili.com/free/intr/{}'.format(i) for i in range(1, 6)],
        'group_xpath': '//*[@id="list"]/table/tbody/tr',
        # 组内xpath,提取ip port area
        'detail_xpath': {
            'ip': './td[1]/text()',  # //*[@id="list"]/table/tbody/tr[1]/td[1]
            'port': './td[2]/text()',
            'area': './td[5]/text()'
        }
    }

    # spider = BaseSpider(**config)
    # for proxy in spider.get_proxies():
    #    print(proxy)
    # urls = ['https://www.kuaidaili.com/free/intr/{}'.format(i) for i in range(1, 6)]
    # for url in urls:
    header = get_request_headers()
    print(header)
    response = requests.get('https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn=3'
                            '&rn=10&from_mid=1&&oe=utf-8', headers=header)

    print(response.content.decode())
