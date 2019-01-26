# coding=utf-8
from pymongo import MongoClient


class MongoHelper:
    def __init__(self, host="127.0.0.1", port=27017, db="test", collection="t1"):
        """
        初始化一个MongHelp类
        :param host: ip
        :param port: 端口
        :param db: 数据库名称
        :param collection: 集合名称
        """
        self.client = MongoClient(host=host, port=port)
        self.collection = self.client[db][collection]

    def insert_one(self, data):
        ret = self.collection.insert(data)
        print(ret)

    def insert_many(self, data_list):
        for data in data_list:
            self.collection.insert(data)
    def find(self,qure=None):
        cursor = self.collection.find(qure)
        for c in cursor:
            print(c)

# m=MongoHelper()
# m.insert_many([{"name":"python11"},{"name":"python12"}])
# m.find()
