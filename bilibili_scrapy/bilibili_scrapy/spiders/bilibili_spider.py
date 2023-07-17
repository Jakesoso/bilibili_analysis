import re

import scrapy
from bilibili_scrapy.items import BilibiliScrapyItem

# get all categories
category_dict = {
    0: '全站', 1: '动画', 3: '音乐', 129: '舞蹈', 4: '游戏', 36: '知识', 188: '科技',
    234: '运动', 223: '汽车', 160: '生活', 211: '美食', 217: '动物', 119: '鬼畜',
    155: '时尚', 5: '娱乐', 181: '影视'
}

# get what
is_get_ranking_list_video = True
is_get_weekly_list_video = True
is_get_bulletScreen = True  # whether bullet screen is needed


class BilibiliSpider(scrapy.Spider):
    name = "bilibili_spider"
    allowed_domains = ["bilibili.com"]

    # entry
    def start_requests(self):
        # get ranking list video
        # 爬取排行榜
        if is_get_ranking_list_video:
            for key, value in category_dict.items():
                next_url = f'https://api.bilibili.com/x/web-interface/ranking/v2?rid={key}&type=all'
                yield scrapy.Request(url=next_url, callback=self.parse, meta={'category': value})

        # get weekly list
        # 爬取每周必看列表
        if is_get_weekly_list_video:
            # get weekly list 每周必看列表
            url = "https://api.bilibili.com/x/web-interface/popular/series/list"
            yield scrapy.Request(url=url, callback=self.get_list_video)

    # get weekly list
    def get_list_video(self, response):
        # get info json
        weekly_list_json = response.json()
        list_info = weekly_list_json['data']['list']

        for list in list_info:
            meta = {'weekly_id': list['number'],
                    'weekly_sub': list['subject'],
                    'weekly_name': list['name']
                    }
            # skip
            if list['number'] != 38 and list['number'] != 143:
                next_url = f"https://api.bilibili.com/x/web-interface/popular/series/one?number={list['number']}"
                yield scrapy.Request(url=next_url, callback=self.parse, meta=meta)

    # get video info
    def parse(self, response):
        # get info json
        rank_json = response.json()
        video_info = rank_json['data']['list']

        # get unique element
        category = -1
        weekly_id = -1
        weekly_sub = -1
        weekly_name = -1

        # set unique element
        if 'category' in response.meta.keys():
            category = response.meta['category']
        elif 'weekly_id' in response.meta.keys():
            weekly_id = response.meta['weekly_id']
            weekly_sub = response.meta['weekly_sub']
            weekly_name = response.meta['weekly_name']

        # set video item
        rank = 0
        for video in video_info:
            # every loop has a separate video item to avoid some mistakes
            video_item = BilibiliScrapyItem()

            # rank info
            rank = rank + 1
            video_item['rank'] = rank
            video_item['category'] = category

            # video info
            video_item['title'] = video['title']
            video_item['author'] = video['owner']['name']

            video_item['tag'] = video['tname']
            video_item['duration'] = video['duration']
            video_item['pubdate'] = video['pubdate']

            video_item['views'] = video['stat']['view']
            video_item['likes'] = video['stat']['like']
            video_item['coins'] = video['stat']['coin']
            video_item['favorite'] = video['stat']['favorite']
            video_item['shares'] = video['stat']['share']
            video_item['bulletScreen_cnt'] = video['stat']['danmaku']
            video_item['video_url'] = f"https://www.bilibili.com/video/{video['bvid']}"
            video_item['bulletScreen_url'] = f"https://comment.bilibili.com/{video['cid']}.xml"

            # weekly info
            video_item['weekly_id'] = weekly_id
            video_item['weekly_sub'] = weekly_sub
            video_item['weekly_name'] = weekly_name

            # up info
            video_item['up_mid'] = video['owner']['mid']
            video_item['up_name'] = video['owner']['name']
            video_item['up_face'] = video['owner']['face']

            # bullet screen is needed
            if is_get_bulletScreen:
                # get bullet screen content
                # dont_filter=True : some videos will be included in two categories,
                # that will cause same url request and will be filtered.
                yield scrapy.Request(video_item['bulletScreen_url'],
                                     callback=self.get_bulletScreen, meta={'video_item': video_item}, dont_filter=True)
            # bullet screen is not needed
            else:
                yield video_item

    # get bullet screen
    def get_bulletScreen(self, response):
        video_item = response.meta['video_item']
        video_item['bulletScreen'] = re.findall('<d p=".*?">(.*?)</d>', response.text)
        yield video_item
