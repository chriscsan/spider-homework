# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: quchong.py

import time
from pymongo import MongoClient

# 初始化MongoDB
conn = MongoClient('127.0.0.1', 27017)
db = conn['study']
collection = db['bilibili']

group = {
     '$group': { 'result': {'aid': '$aid'},'_id':{'$push': '$_id'}, 'count': {'$sum': 1}}
}

match = {
    '$match': {'count': {'$gt': 1}}
}
a = collection.aggregate([group, match])
l = list(a)
# l.sort(key=lambda item: item['_id']['aid'])
i = 0
for item in l:
    i += 1
    _id = item['_id'][0]
    collection.delete_one({'_id': id})
    print(item)
print(i)
