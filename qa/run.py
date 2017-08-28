from twisted.internet import reactor,defer
import scrapy
import sys
import os
sys.path.insert(0, os.getcwd())#将qa目录插入到环境变量里面，这样就能找到此包
from twisted.internet import reactor, defer, task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from qa.spiders.qa_spider import QASpider
from qa.utils import EmailUtil
from qa.utils import Mongo_utils
from qa.utils import get_index_from_disk



def get_statistics_info():
    info = {}
    mongo = Mongo_utils(db='mafengwo',collection='ma_feng_wo_qa')
    info['urls_requried_num'] = mongo.get_count() #Mongodb已经爬取的url数量
    info['index'] = get_index_from_disk()
    info = '[mafengwo] Url index is {}.\n' \
           '[mafengwo] We has requested {} url.\n'.format(info['index'],info['urls_requried_num'])
    return info

def main():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    setting = get_project_settings()
    runner = CrawlerRunner(setting)

    runner.crawl(QASpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    if setting.get('MAIL_ALERT'):
        lc = task.LoopingCall(EmailUtil.send_email, content_getter_func=get_statistics_info)
        lc.start(interval=setting.get('EMAIL_INTERNAL'), now=False)  # 每24小时发送统计信息
    reactor.run()


if __name__ == '__main__':
    main()