from lxml import etree

from domain import Proxy
from utils.http import get_request_headers
from core.proxy_spider.spider_base import BaseSpider
import time
import random
import requests
import re
import js2py


# 实现快代理的爬虫 https://www.kuaidaili.com/free/inha/1
# 反爬
class KuaiSpider(BaseSpider):
    # url列表
    urls = ['https://www.kuaidaili.com/free/intr/{}'.format(i) for i in range(1, 6)]
    # 分组xpath，用于获取代理ip信息的标签列表
    # //*[@id="list"]/table/tbody/tr[1]/td[1]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内xpath,提取ip port area
    detail_xpath = {
        'ip': './td[1]/text()',  # //*[@id="list"]/table/tbody/tr[1]/td[1]
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

    # 这个网站刚问时间间隔太短了会报错，网站的反爬手段
    # 重写get_page_from_url
    def get_page_from_url(self, url):
        # 每次等待一会
        time.sleep(random.uniform(1, 3))
        # 调用父类的方法
        return super().get_page_from_url(url)


# 实现https://www.7yip.cn/free/代理ip的爬虫
class QiyunSpider(BaseSpider):
    # url列表
    urls = ['https://www.7yip.cn/free/?action=china&page={}'.format(i) for i in range(1, 11)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '//*[@id="content"]/section/div[2]/table/tbody/tr/'  # //*[@id="content"]/section/div[
    # 2]/table/thead/tr/th[1]
    # 组内xpath,提取ip port area
    detail_xpath = {
        'ip': './td[1]/text()',  # //*[@id="content"]/section/div[2]/table/tbody/tr[1]/td[1]/text()
        'port': './td[2]/text()',  # //*[@id="content"]/section/div[2]/table/tbody/tr[1]/td[2]/text()
        'area': './td[5]/text()'  # //*[@id="content"]/section/div[2]/table/tbody/tr[1]/td[5]/text()
    }


# 实现https://www.89ip.cn/index_4.html代理ip的爬虫
class EightnineSpider(BaseSpider):
    # url列表
    urls = ['https://www.89ip.cn/index_{}.html'.format(i) for i in range(1, 8)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '/html/body/meta"utf-8"/div[3]/div[1]/div/div[1]/table/tbody/tr'
    # 组内xpath,提取ip port area
    detail_xpath = {
        'ip': './td[1]/text()',  # /html/body/meta"utf-8"/div[3]/div[1]/div/div[1]/table/tbody/tr[1]/td[1]
        'port': './td[2]/text()',  # /html/body/meta"utf-8"/div[3]/div[1]/div/div[1]/table/tbody/tr[1]/td[2]
        'area': './td[3]/text()'  # /html/body/meta"utf-8"/div[3]/div[1]/div/div[1]/table/tbody/tr[1]/td[3]
    }


# 实现Ip3366代理的爬虫 http://www.ip3366.net/free/?stype=1&page=1
# 可以使用
class Ip3366Spider(BaseSpider):
    # url列表
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for i in range(1, 3) for j in range(1, 11)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内xpath,提取ip port area
    detail_xpath = {
        'ip': './td[1]/text()',  # //*[@id="list"]/table/tbody/tr[1]/td[1]
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


# 实现yqie代理的爬虫 http://ip.yqie.com/proxygaoni/index_3.htm
# 可以使用
class YqieSpider(BaseSpider):
    # url列表
    urls = ['http://ip.yqie.com/proxygaoni/index_{}.htm'.format(i) for i in range(1, 11)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '//*[@id="GridViewOrder"]/tr[position()>1]'  # //*[@id="GridViewOrder"]/tbody/tr[1]/th[2]
    # 组内xpath,提取ip port area
    detail_xpath = {
        'ip': './td[2]/text()',  # //*[@id="GridViewOrder"]/tbody/tr[2]/td[2]
        'port': './td[3]/text()',  # //*[@id="GridViewOrder"]/tbody/tr[2]/td[3]
        'area': './td[4]/text()'  # //*[@id="GridViewOrder"]/tbody/tr[2]/td[4]
    }


# 实现http://www.66ip.cn/代理ip的爬虫
# 可以使用
# http://www.66ip.cn/原来有反爬手段  js加密+cookie验证
# 现在没有反爬手段了
class SixsixSpider(BaseSpider):
    # url列表
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 11)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'  # //*[@id="main"]/div/div[1]/table/tbody/tr[
    # 1]/td[1]
    # 组内xpath,提取ip port area
    detail_xpath = {
        'ip': './td[1]/text()',  # //*[@id="main"]/div/div[1]/table/tbody/tr[2]/td[1]
        'port': './td[2]/text()',  # //*[@id="main"]/div/div[1]/table/tbody/tr[2]/td[2]
        'area': './td[3]/text()'  # //*[@id="main"]/div/div[1]/table/tbody/tr[2]/td[3]
    }

    # 重写方法，解决js加密+cookie验证反爬问题
    def get_page_from_url(self, url):
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        # 有js加密反爬
        if response.status_code == 521:
            # 生成cookie信息，再携带cookie发送请求
            # 生成 '_ydclearance' cookie信息
            # 1.确定'_ydclearance'是从哪里来的
            # 观察发现不是通过服务器相应设置过来的，那就是通过js生成的
            # 2.第一次发送请求的页面中，有一个生成这个cookie的js，执行这段js，生成需要的cookie
            # 这段js时经过加密处理的js，真正的js在 “po”中
            # 3.提取 ‘jp（107）’ 调用函数的方法以及函数
            result = re.findall('window.onload=setTimeout\("(.+?)",200\);\s*(.+?)\s*</script> ',
                                response.content.decode('GBK'))
            # 4.执行js时候，返回真正要执行的js代码
            # 把eval····替换 return po
            func_str = result[0][1]
            func_str = func_str.replace('eval("qo=eval;qo(po);")', 'return po')
            # 5.获取执行js环境
            context = js2py.EvalJs()
            # 6.加载执行func_str
            context.execute(func_str)
            # 7.执行这个方法生成需要的js
            context.execute('code={}'.format(result[0][0]))
            # 8.提取到cookie
            cookie_str = re.findall("document.cookie='(.+?);", context.code)
            # 9.带上cookie再次发送请求
            headers['Cookie'] = cookie_str
            response = requests.get(url, headers=headers)
            return response.content.decode('GBK')
        # 没有js加密反爬，或者已经生成了cookie，可以直接获取页面了
        else:
            return response.content.decode('GBK')
        # return response.content.decode()


# 实现xila代理的爬虫 http://www.xiladaili.com/gaoni/2/
class XilaSpider(BaseSpider):
    # url列表
    urls = ['http://www.xiladaili.com/gaoni/{}/'.format(i) for i in range(1, 20)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '/html/body/div/div[3]/div[2]/table/tbody/tr'
    # 组内xpath,提取ip port area
    detail_xpath = {  # /html/body/div/div[3]/div[2]/table/tbody/tr[1]/td[1]
        'ip_port': './td[1]/text()',  # /html/body/div/div[3]/div[2]/table/tbody/tr[4]/td[1]
        'area': './td[4]/text()'  # /html/body/div/div[3]/div[2]/table/tbody/tr[6]/td[4]
    }

    # 重写从页面提取数据，封装为proxy对象
    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        # 获取包含代理ip信息的标签列表
        trs = element.xpath(self.group_xpath)
        # 遍历trs，获取代理ip相关ip信息
        for tr in trs:
            ip_port = self.get_first_from_list(tr.xpath(self.detail_xpath['ip_port']))
            ip = ip_port.split(":")[0]
            port = ip_port.split(":")[1]
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            yield proxy


# 实现jiangxianli代理的爬虫 https://ip.jiangxianli.com/?page=2
# 可以使用
class JiangXianLiSpider(BaseSpider):
    # url列表
    urls = ['https://ip.jiangxianli.com/?page={}'.format(i) for i in range(1, 6)]
    # 分组xpath，用于获取代理ip信息的标签列表
    group_xpath = '/html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr'  #
    # 组内xpath,提取ip port area
    detail_xpath = {  # /html/body/div[1]/div[2]/div[1]/div[1]/table/thead/tr/th[1]
        'ip': './td[1]/text()',  # /html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td[1]
        'port': './td[2]/text()',  # /html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[2]
        'area': './td[5]/text()'  # /html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[5]
    }


if __name__ == '__main__':
    # urls = ['https://www.7yip.cn/free/?action=china&page={}'.format(i) for i in range(1, 11)]
    # print(urls)
    # spider = KuaiSpider()
    # spider = Ip3366Spider()
    # spider = YqieSpider()
    # spider = SixsixSpider()
    # spider = QiyunSpider()
    # spider = EightnineSpider()
    # spider = XilaSpider()
    spider = JiangXianLiSpider()
    for proxy in spider.get_proxies():
        print(proxy)
