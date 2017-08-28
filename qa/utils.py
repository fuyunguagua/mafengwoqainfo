import json
import pymongo
import re
import requests
from qa import redis
from qa.settings import MONGO_CONF
from qa import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class Mongo_utils(object):
    def __init__(self,db=None,collection=None):
        #from ipdb import set_trace
        #set_trace()
        #链接mongo
        self.mongo_host = MONGO_CONF.get('host')
        self.mongo_port = MONGO_CONF.get('port')
        self.mongo_user = MONGO_CONF.get('user',None)
        self.mongo_pass = MONGO_CONF.get('passwd',None)
        self.mongo_client = pymongo.MongoClient(
            host=self.mongo_host,port=self.mongo_port
        )
        if isinstance(db,str):
            self.db = db
            self.mongo_db = self.mongo_client[self.db]
        if isinstance(collection,str):
            self.collection = collection
            self.collection = self.mongo_db[self.collection]

    def get_dbs(self):
        '''获取所有的数据库'''
        return self.mongo_client.database_names()


    def get_collections(self):
        '''
        获取所有的集合
        '''
        return self.mongo_db.collection_names()

    def insert_data(self,data):
        if isinstance(data,list):
            self.collection.insert_many(data)
        elif isinstance(data,dict):
            self.collection.insert(data)
        else:
            pass

    def get_data(self,**condition):
        '''
        获取数据
        '''
        return self.collection.find(condition)

    def delete_data(self,**condition):
        '''
        删除数据
        '''
        return self.collection.remove(condition)

    def get_count(self,**condition):
        '''
        获取数据量
        :param condition:
        :return:
        '''
        return self.collection.find(condition).count()



class EmailUtil(object):

    @staticmethod
    def send_email(content_getter_func):
        #如果设置了邮箱提醒
        if settings.MAIL_ALERT:
            sender = settings.MAIL_FROM
            receiver = settings.MAIL_TO
            smtpserver = settings.MAIL_HOST
            username = settings.MAIL_USER
            password = settings.MAIL_PASS
            port = settings.MAIL_PORT
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = 'scrapy'

            content = content_getter_func() #get
            text = MIMEText(content, _subtype='plain', _charset='gb2312')
            msgRoot.attach(text)

            smtp = smtplib.SMTP_SSL()
            smtp.connect(smtpserver, port)
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msgRoot.as_string())
            smtp.quit()


def get_index_from_disk():
    try:
        with open('./qa/log/index.log','r') as f:
            return f.readline()
    except FileNotFoundError:
        return str(1000000)


def save_index_to_disk(index):
    with open('./qa/log/index.log', 'w') as f:
        f.write(str(index))
