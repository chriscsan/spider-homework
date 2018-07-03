
'''
标签请求链接: https://api.bilibili.com/x/tag/archive/tags?aid=25533190                 aid ---> av_id
视频信息： https://api.bilibili.com/x/web-interface/newlist?rid=171&pn=1&ps=20         rid ---> tag_id, pn ---> page_number, ps ---> page_size     


'''
a = {
    aid: 25533304,                                 #aid
    tid: 171,                                      # typeid
    tname: "电子竞技",                              # typename
    title: "王者荣耀：关羽装备一匹马",               # title
    pubdate: 1529853152,                           # 发布时间
    desc: ''                                       # 视频描述
    attribute: 16384,                              # 原文件大小
    duration: 915,                                 # 时长(秒)
    mid: 194537167,                                # 作者uid
    name: "韶白泽",                                # 作者名字
    aid: 25533304,                                 # 视频aid
    view: 2,                                       # 观看数量
    danmaku: 0,                                    # 弹幕数量
    reply: 0,                                      # 评论数量
    favorite: 0,                                   # 收藏数量
    coin: 0,                                       # 投币数量
    share: 1,                                      # 被分享次数
    like: 0,                                       # 喜欢该视频数
    dislike: 0                                     # 不喜欢该视频数



'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Host': 'www.bilibili.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
