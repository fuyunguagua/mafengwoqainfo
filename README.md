###爬取马蜂窝的问答信息


***为什么说它是分布式？***

因为它将提取的url放在redis里，每个实例来取url之后，就删掉。
相当于生产者消费者模式。

###用法：
将项目导入到pycharm中，在本地安装好redis和mongodb，运行run.py
在setting.py设置相关的字段
###已实现：
利用selenium和phantomjs抓取动态加载的行程信息。
将爬取到的行程的概览信息存入到mongodb中
将最终的行程信息存入到mongodb中。
每隔固定时间给自己的邮箱发送爬虫的统计信息。
###TODO:
实现增量爬取。
