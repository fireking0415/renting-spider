# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient


class RentingspiderPipeline(object):

    def __init__(self):
        # 创建mongodb数据库链接
        client = MongoClient(host='localhost', port=27017)

        # 指定使用的数据库
        mydb = client['renting']

        # 指定用来存贮爬取数据的数据表
        self.sheet = mydb['tb_multi_renting']

    def process_item(self, item, spider):
        data = dict(item)
        self.sheet.insert(data)
        return item
