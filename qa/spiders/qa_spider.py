from scrapy import Spider
from scrapy import Request
from qa.restract import Restractor
from qa.items import QAItem
from qa.utils import save_index_to_disk
from qa.utils import get_index_from_disk

class QASpider(Spider):
    name = 'qaspider'
    start_urls = ['http://www.mafengwo.cn/wenda/detail-1000000.html']
    allowed_domains = ['mafengwo.cn']
    def __init__(self):
        self.index = int(get_index_from_disk())

    def parse(self, response):
        #构造下次请求url
        def get_next_url():
            self.index += 1
            return "http://www.mafengwo.cn/wenda/detail-"+str(self.index)+".html"
        #如果页面存在就取数据
        if response.status is 200:
            item = QAItem()
            item['data'] = Restractor.restract_qa_info(response.text)
            yield item
        #记录当前爬取位置
        save_index_to_disk(self.index)
        yield Request(get_next_url())
