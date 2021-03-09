# 实现代理池的校验模块
# 检查代理ip速度，匿名程度以及支持的协议类型
import time
import requests
import json
from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy


# 用于检查指定 代理ip 匿名程度  响应速度 支持协议类型
# proxy: 代理ip模型对象
def check_proxy(proxy):
    # 代理ip字典
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }

    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)

    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy


def __check_http_proxies(proxies, is_http=True):
    # 匿名程度 :高匿：0  匿名：1 透明：2
    nick_type = -1
    # 响应速度 s
    speed = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        # 获取开始时间
        start = time.time()

        # 对http://httpbin.org/get 或者https://httpbin.org/get 发送请求，获取响应
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)

        if response.ok:
            # 计算响应速度
            speed = round(time.time() - start, 2)
            # 测试匿名程度
            # 把响应的json字符串转换为字典。
            dic = json.loads(response.text)
            # 获取来源IP：origin
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            # 1.如果响应中有 ',' 分隔开的两个IP就是透明代理IP
            if ',' in origin:
                nick_type = 2
            # 2.如果相应的headers中包含 Proxy-Connection说明是匿名代理IP
            elif proxy_connection:
                nick_type = 1
            # 3.否则就是高匿名代理IP
            else:
                nick_type = 0
            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as ex:
        logger.debug(ex)
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy('103.152.5.80', port='8080')
    print(check_proxy(proxy))
