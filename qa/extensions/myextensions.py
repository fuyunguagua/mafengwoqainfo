import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from qa.utils import EmailUtil
from qa.utils import get_index_from_disk
from qa import settings
logger = logging.getLogger(__name__)

class SpiderOpenCloseLogging(object):

    def __init__(self):
        pass
    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwis

        # instantiate the extension object
        ext = cls()

        # 将函数与信号绑定
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s", spider.name)
        if settings.MAIL_ALERT:
            EmailUtil.send_email(lambda:'[mafengwo] Spider start at index {}'.format((get_index_from_disk()))) # 关掉spider时，发送邮件
    def spider_closed(self, spider):
        logger.info("closed spider %s", spider.name)
        if settings.MAIL_ALERT:
            EmailUtil.send_email(lambda:'[mafengwo] Spider stopped at index {}'.format((get_index_from_disk())))  # 关掉spider时，发送邮件
    def item_scraped(self, item):
        pass