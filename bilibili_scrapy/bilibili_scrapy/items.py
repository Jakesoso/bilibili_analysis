# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # basic rank info
    rank = scrapy.Field()               # 视频排名
    category = scrapy.Field()           # 视频分区

    # basic video info
    title = scrapy.Field()              # 视频标题
    author = scrapy.Field()             # 视频作者
    tag = scrapy.Field()                # 视频标签
    duration = scrapy.Field()           # 视频时长
    pubdate = scrapy.Field()            # 发布时间
    views = scrapy.Field()              # 播放数
    likes = scrapy.Field()              # 点赞数
    coins = scrapy.Field()              # 投币数
    favorite = scrapy.Field()           # 收藏数
    shares = scrapy.Field()             # 分享数
    bulletScreen_cnt = scrapy.Field()   # 弹幕数
    video_url = scrapy.Field()          # 视频链接
    bulletScreen_url = scrapy.Field()   # 弹幕链接
    bulletScreen = scrapy.Field()       # 弹幕内容

    # weekly list info
    weekly_id = scrapy.Field()          # 每周必看期数
    weekly_sub = scrapy.Field()         # 每周必看主题
    weekly_name = scrapy.Field()        # 每周必看名字

    # up info
    up_mid = scrapy.Field()             # uid
    up_name = scrapy.Field()            # 用户名
    up_face = scrapy.Field()            # 头像