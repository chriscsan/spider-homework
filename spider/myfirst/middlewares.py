# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests


class MyfirstSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyfirstDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.



        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ChangeProxy(object):
    '''
    1) 什么时候需要切换ip
        ip被ban了, 被拉黑了,无法继续使用了
    2) 如何优秀的切换IP
        A) 代理IP给我们的API,有限制
        B) 可能我们获取ip之后就失效了
        C) 很有可能一个ip使用多次才会被办ban
    '''
    def __init__(self):
        # self.f = open('a.txt', 'r')
        self.get_url = 'http://s.zdaye.com/?api=201806271304317790&px=2'
        self.test_url = 'http://ip.chinaz.com/getip.aspx'
        self.list = []
        #默认的是用来记录使用ip的个数,或者是目前正在使用的第几个ip
        # 有不有ip
        # 第一次访问
        self.count = -1
        # 每个ip的使用次数
        self.eve_count = 0

    def get_data(self):
        print('获取proxy')
        data = requests.get(url=self.get_url).text;

        if self.list:
            self.list.clear()

        for proxy in data.split('\n'):
            self.list.append(proxy)
    def change_proxy(self, request):
        request.meta['proxy'] = 'http://{}'.format(self.list[self.count].strip())
        print('******************************proxy: ',  self.list[self.count])
        # request.mate['download_timeout'] = 5
    def yanzhen(self):
        
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>prxoy: ', self.list[self.count])
        requests.get(self.test_url, proxies ={'http': self.list[self.count].strip()}, timeout=2)
        print('验证成功: ', self.list[self.count])

    def ifUsed(self, request):
        try:
            print(1111111)
            self.yanzhen()
            print(2222222)
            self.change_proxy(request)
            print(3333333)
        except:
            print('验证失败....')
            if self.count == -1 or self.count > 4:
                print(44444444)
                self.count = 0
                self.get_data()
            else:
                self.count += 1
                print(5555555)
            self.ifUsed(request)
        print('发出请求....')
        
    def process_request(self, request, spider):
        # proxy = random.choice(self.IPPOOL)
        if self.count == -1 or self.count > 4:
            self.count = 0
            self.get_data()
        print('按时的黄金卡上的 哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈 哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈')
        if self.eve_count >= 5:
            self.count += 1
            self.eve_count = 0
        else:
            # self.change_proxy(request)
            self.eve_count += 1
            # self.count = 1
        print('按时的黄金卡上的 哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈 哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈')
        self.ifUsed(request)
        