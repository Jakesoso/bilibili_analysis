
# script for running Scrapy
# 2023.6.11

from scrapy.cmdline import execute

if __name__ == '__main__':
    execute('scrapy crawl bilibili_spider'.split())