from settings import MAX_SCORE


class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        self.ip = ip  # 代理的ip地址
        self.port = port  # 代理的ip的端口号
        self.protocol = protocol  # 代理ip支持的协议，http是0，https是1，http+https是2
        self.nick_type = nick_type  # 代理ip的匿名程度，高匿：0 ，匿名：1 ，透明：2
        self.speed = speed  # 代理ip的相应速度 单位s
        self.area = area  # 代理ip所在的区域
        self.score = score  # 代理ip的评分，用于衡量代理IP的可用性
        # 默认分值通过配置文件配置，进行代理ip可用性检查时，没遇到一次请求失败就减一，见到0就删掉
        self.disable_domains = disable_domains  # 不可用的域名列表，有些代理ip在某些域名下不可用，但是在其他域名可用

    def __str__(self):
        return str(self.__dict__)
