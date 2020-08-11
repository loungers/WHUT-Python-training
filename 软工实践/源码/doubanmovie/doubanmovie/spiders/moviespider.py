# -*- coding: utf-8 -*-
import scrapy
from doubanmovie.items import DoubanmovieItem

class MoviespiderSpider(scrapy.Spider):
    name = 'moviespider'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        currentpPage_movie_item = response.xpath('//div[@class="item"]')
        for movie_item in currentpPage_movie_item:
            # 创建一个Movie对象
            movie = DoubanmovieItem()
            # 获取电影排名并赋值rank属性
            movie['rank'] = movie_item.xpath('div[@class="pic"]/em/text()').extract()
            # 获取电影名称并赋值title属性
            movie['title'] = movie_item.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]/text()').extract()
            # 获取电影海报地址并赋值pic_url属性
            movie['pic_url'] = movie_item.xpath('div[@class="pic"]/a/img/@src').extract()
            # 将封装好的一个电影信息添加到容器中,yield作用是创建一个列表并添加元素
            yield movie
            pass
        
        # 下一页请求跳转，实现自动翻页
        nextPage = response.xpath('//span[@class="next"]/a/@href')
        # 判断nextPage是否有效（无效代表当前页面为最后一页）
        if nextPage:
            # 获取nextPage中的下一页链接地址并加入到respones对象的请求地址中
            url = response.urljoin(nextPage[0].extract())
            # 发送下一页请求并调用parse()函数继续解析
            yield scrapy.Request(url, self.parse)
        pass
