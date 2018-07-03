# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: fenxi.py

from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from pyecharts import Pie
from pyecharts import Bar
from pyecharts import Line


from os import path 
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator 
import pickle 
import jieba 
import codecs


# 初始化mongo_db
conn = MongoClient('127.0.0.1', 27017)
db = conn['study']
coll = db['bilibili']

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


# 分析
#  视频分类信息  饼图
def paint_video_info():
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        {'$group':{'_id':'$type_name', 'video_number':{'$sum': 1}}},
        # {'$project':{'type_name':'$type_name', 'title':'$title','danmaku':'$danmaku'}},
        {'$sort':{'danmaku':-1}},
        {'$limit': 30}
    ])
    df = pd.DataFrame(list(result))
    # 画图
    attr = []
    data = []
    pie = Pie('视频分类信息图')

    for eve_data in df.values:
        attr.append(eve_data[0])
        data.append(eve_data[1])
    pie.add("", attr, data, is_label_show=True, width=1200, height=600)
    pie.render('./视频分区信息饼图.html')

def zuiduo(field_name, graph_title):
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        # {'$group':{'_id':'$type_name', 'video_number':{'$sum': 1}}},
        {'$project':{field_name: '$'+field_name, 'aid': '$aid'}},
        {'$sort':{field_name:-1}},
        {'$limit': 30}
    ])
    df = pd.DataFrame(list(result))
     # 初始化数据
    attr = []
    data = []
    bar = Bar(graph_title)

    for eve_data in df.head(15).values:
        print(eve_data)
        attr.append('id'+str(eve_data[1]))
        data.append(eve_data[2])
    # 绘图
    bar.add("rank", attr, data, is_stack=True, width=1200, height=600)
    print(attr)
    print(data)
    bar.render('./'+graph_title+'.html')


# 作者最多
def author_zuiduo(graph_title, field_name = ''):
    result  = None
    if(field_name != ''):
        result = coll.aggregate([
            # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
            {'$group':{'_id':'$author_name', 'total_coin':{'$sum': '$'+field_name}}},
            # {'$project':{'author_name': '$author_name'}},
            {'$sort':{'total_coin':-1}},
            {'$limit': 30}
        ])
    else:
        result = coll.aggregate([
            # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
            {'$group':{'_id':'$author_name', 'video_number':{'$sum': 1}}},
            # {'$project':{'author_name': '$author_name'}},
            {'$sort':{'video_number':-1}},
            {'$limit': 30}
        ])
    df = pd.DataFrame(list(result))
     # 初始化数据
    attr = []
    data = []
    bar = Bar(graph_title,width=1200, height=600)

    for eve_data in df.head(15).values:
        attr.append(eve_data[0][:3])
        data.append(eve_data[1])
    # 绘图
    bar.add("rank", attr, data, label_color=['rgb(54, 70, 85)'], is_stack=True, width=1200, height=600)
    bar.render('./'+graph_title+'.html')

def draw_wordcloud():
    content = ''
    results = coll.find().limit(10000)
    # df = pd.DataFrame(list(results))

    for result in results:
        # print(result[1])
        content += result['desc']
    cut_content = ' '.join(jieba.cut(content))
    cut_content += ' '

    d = path.dirname(__file__)
    print(d)
    backgroud_image = plt.imread(d+'/python.jpg') 
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        # font_path="hwxk.ttf",
        font_path='C:\Windows\Fonts\STZHONGS.TTF',
        #设置背景色
        background_color='white',
        #词云形状
        mask=backgroud_image,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=200,
        # width=1000,
        # height=1000
    )
    word_cloud = cloud.generate(cut_content) # 产生词云
    word_cloud.to_file(d+"/wordcloud.jpg") #保存图片
    #  #  显示词云图片
    # plt.imshow(word_cloud)
    # plt.axis('off')
    # plt.show()

def fenbu(graph_title):
    result = None
    attr = ['0~100', '101~1w', '1w~100w', '100w+']
    data = []
    for i in range(0, 7, 2):
        result = coll.aggregate([
            # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
            {'$group':{'_id':'$author_name', 'total_view':{'$sum': '$view'}}},
            # {'$project':{'author_name': '$author_name'}},
            {'$match': {'total_view': {'$gte': 10**i-1, '$lte': 10**(i+2)}}}
        ])
        data.append(len(list(result)))
    pie = Pie(graph_title)
    pie.add("", attr, data, is_label_show=True, width=1200, height=600)
    pie.render('./'+graph_title+'.html')

def dura_denbu(graph_title):
    result = None
    attr = ['0~1min', '1min~5min', '5min~10min', '10min~20min', '20min+']
    data = []
    # '0~1min'
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        # {'$group':{'_id':'$author_name', 'total_view':{'$sum': '$view'}}},
        # {'$project':{'author_name': '$author_name'}},
        {'$match': {'video_duration': {'$lt': 60}}}
    ])
    data.append(len(list(result)))
    # 1min~5min'
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        # {'$group':{'_id':'$author_name', 'total_view':{'$sum': '$view'}}},
        # {'$project':{'author_name': '$author_name'}},
        {'$match': {'video_duration': {'$gte': 60, '$lt': 300}}}
    ])
    data.append(len(list(result)))
    # '5min~10min'
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        # {'$group':{'_id':'$author_name', 'total_view':{'$sum': '$view'}}},
        # {'$project':{'author_name': '$author_name'}},
        {'$match': {'video_duration': {'$gte': 300, '$lt': 600}}}
    ])
    data.append(len(list(result)))
    # '10min~20min'
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        # {'$group':{'_id':'$author_name', 'total_view':{'$sum': '$view'}}},
        # {'$project':{'author_name': '$author_name'}},
        {'$match': {'video_duration': {'$gte': 600, '$lt': 1200}}}
    ])
    data.append(len(list(result)))
    # '20min+'
    result = coll.aggregate([
        # {'$project':{'c':1, 't':1, 'readers':1, 'a':{'$divide':['$t','$c']}}},
        # {'$group':{'_id':'$author_name', 'total_view':{'$sum': '$view'}}},
        # {'$project':{'author_name': '$author_name'}},
        {'$match': {'video_duration': {'$gte': 1200}}}
    ])
    data.append(len(list(result)))
    pie = Pie(graph_title)
    pie.add("", attr, data, is_label_show=True, width=1200, height=600)
    pie.render('./'+graph_title+'.html')

def time_qushi(graph_title):
    result = None
    attr = ['6月19','6月20','6月21','6月22','6月23','6月24','6月25','6月26','6月27','6月28']
    data = []
    # pipe = [
    #     {'$sort': {'publish_time': -1},'allowDiskUse':True },
    #     {'$limit': 10}
    # ]
    # 1530085564
    for i in range(10):
        pipe = [
            {'$match': {'publish_time':{'$lte': 1530085564-i*24*60*60, '$gt': 1530085564-(i+1)*24*60*60}}}
        ]
        data.append(len(list(coll.aggregate(pipe))))
    
    # from pyecharts import Line

    line = Line(graph_title)
    line.add("", attr, data, iis_stack=True, is_label_show=True, width=1200, height=600)
    line.render('./'+graph_title+'.html')
    # print(len(data))
    # print(data)
#  视频分区信息饼图
# paint_video_info()
# 弹幕量排名
zuiduo('danmaku', '弹幕量排名')
# 观看量排名
zuiduo('view', '观看量排名')
# 硬币量排名
zuiduo('danmaku', '硬币量排名')
# # 最不受欢迎排名
# zuiduo('danmaku', '最不受欢迎排名')
# # 上传视频最多的up主排行 TOP10
# author_zuiduo('上传视频最多的up主排行 TOP10')
# # 收到硬币数量的up主排行 TOP10
# author_zuiduo('收到硬币数量的up主排行 TOP10', 'coin')
# # 总观看量up主排行 TOP10
# author_zuiduo('总观看量up主排行 TOP10', 'view')
# # 生成title词云
# # draw_wordcloud()
# # 总观看量up主分布
# fenbu('总观看量up主分布')
# # 视频时长分布
# dura_denbu('视频时长分布')
# # 最近10天每天上传视频数量走势
# time_qushi('最近10天每天上传视频数量走势')







    

