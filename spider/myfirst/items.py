# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyfirstItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VideoItem(scrapy.Item):
    aid            = scrapy.Field()    # 视频id          
    type_id        = scrapy.Field()    # 类型id          
    type_name      = scrapy.Field()    # 类型名字 
    desc           = scrapy.Field()    # 视频简介      
    title          = scrapy.Field()    # 视频名字         
    publish_time   = scrapy.Field()    # 发布时间             
    video_duration = scrapy.Field()    # 视频时长            
    author_id      = scrapy.Field()    # 作者id                 
    author_name    = scrapy.Field()    # 作者名字           
    view           = scrapy.Field()    # 观看数量       
    danmaku        = scrapy.Field()    # 弹幕数量             
    reply          = scrapy.Field()    # 评论数量       
    favorite       = scrapy.Field()    # 收藏数量         
    coin           = scrapy.Field()    # 投币数量      
    share          = scrapy.Field()    # 被分享次数         
    like           = scrapy.Field()    # 喜欢该视频数  
    dislike        = scrapy.Field()    # 不喜欢该视频数     
