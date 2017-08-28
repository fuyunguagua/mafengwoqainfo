#coding=utf-8
import random
from scrapy.http import HtmlResponse
from scrapy import Request
import time
from .spiders.qa_spider import QASpider
from qa import settings
class RandomUserAgent(object):
    def __init__(self,agent):
        self.agents = agent
        self.index = 1000000
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self,request,spider):
        request.headers.setdefault('User_Agent',random.choice(self.agents))







#设置代理
class ProxyMiddleware(object):

    def __init__(self):
        self.proxys = settings.PROXY

    def process_request(self,request,spider):
        proxy = 'http://'+self.proxys[0]
        request.meta['proxy'] = proxy

    def process_response(self,request,response,spider):
        return response



    def process_exception(self,request,exception,spider):
        print(exception)
        new_request = request.copy()
        new_request.meta['proxy'] = 'http://'+random.choice(random.choice(self.proxys))
        return new_request







