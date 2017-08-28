# -*- coding: utf-8 -*-


from qa.utils import Mongo_utils

#处理item,空字段设为无
#去重


class MongoPipeline(object):

    def process_item(self, item, spider):
        collection_name = 'ma_feng_wo_qa'
        Mongo_utils(db='mafengwo', collection=collection_name).insert_data(item['data'])
        return item





