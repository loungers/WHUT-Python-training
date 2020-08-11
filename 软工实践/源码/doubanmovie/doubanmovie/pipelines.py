# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanmoviePipeline(object):
    def process_item(self, item, spider):
        print('排名TOP:' + item['rank'][0])
        print('电影名称:' + item['title'][0])
        return item
