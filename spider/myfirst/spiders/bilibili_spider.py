# -*- coding: utf-8 -*-

import scrapy
import json
import time
from urllib import parse
import re
from myfirst.items import VideoItem

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domain = 'bilibili.com'
    start_urls = [
        # 'http://icanhazip.com/'
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=127&pn=1&ps=20',
        # 'https://api.bilibili.com/x/tag/ranking/archives?tag_id=27398&rid=126&pn=1&ps=50'
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=19&pn=1&ps=50',
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=17&pn=3060&ps=50',
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=65&pn=3017&ps=50',
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=171&pn=540&ps=50',
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=172&pn=1&ps=50',
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=173&pn=1&ps=50',
        # 'https://api.bilibili.com/x/web-interface/newlist?rid=121&pn=1&ps=50',
        'https://api.bilibili.com/x/web-interface/newlist?rid=136&pn=1&ps=50',
    ]

    def parse(self, response):
        # url = 'http://icanhazip.com/'
        current_url = response.url
        data = json.loads(response.text)
        
        # print('*******************************************************************************************************************************************************************************************************')
        if bool(data['data']['archives']):
            # 获取数据
            # print(data['data']['archives'])
            for video in self.get_item(data['data']['archives']):
                yield video

            print('*******************************************************************************************************************************************************************************')
            # 下一页
            query_string = parse.urlparse(current_url).query
            page_num = int(parse.parse_qs(query_string)['pn'][0])
            print(current_url)
            print(page_num)
            next_page = re.sub(r'&pn=\d+', '&pn='+str(page_num+1), current_url)
            # print(next_page)
            yield scrapy.Request(url = next_page, callback=self.parse)

    # 获取数据        
    def get_item(self, data):
        for item in data:
            video = VideoItem()

            video['aid']            = item['aid']
            video['type_id']        = item['tid']
            video['type_name']      = item['tname']
            video['title']          = item['title']
            video['desc']           = item['desc']
            video['publish_time']   = item['pubdate']
            video['video_duration'] = item['duration']
            video['author_id']      = item['owner']['mid']
            video['author_name']    = item['owner']['name']
            video['view']           = item['stat']['view']
            video['danmaku']        = item['stat']['danmaku']
            video['reply']          = item['stat']['reply']
            video['favorite']       = item['stat']['favorite']
            video['coin']           = item['stat']['coin']
            video['share']          = item['stat']['share']
            video['like']           = item['stat']['like']
            video['dislike']        = item['stat']['dislike']
            # print(video)
            yield video
        
