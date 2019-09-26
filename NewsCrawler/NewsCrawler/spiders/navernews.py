# -*- coding: utf-8 -*-
import scrapy
from dateutil.relativedelta import relativedelta
from datetime import date
import pandas as pd
from NewsCrawler.items import NewscrawlerItem


class NavernewsSpider(scrapy.Spider):
    name = 'navernews'
    start_urls = []

    start = (date.today()-relativedelta(years = 0, days =1)) #.strftime('%Y.%m.%d')
    end = (date.today()-relativedelta(days = 1)) #.strftime('%Y.%m.%d')
    query = '삼성전자'
    for date in pd.date_range(start = start, end = end):
        date = date.strftime('%Y%m%d')
        url = 'https://search.naver.com/search.naver?where=news&query={0}&sort=0&pd=3&ds={1}&de={1}'.format(query, date)
        start_urls.append(url)

    def parse(self, response):
        for tag in response.css('div.news ul.type01 li'):
            if tag.css('dd.txt_inline a._sp_each_url').get():
                href = tag.css('dd.txt_inline a::attr(href)').get()
                yield response.follow(href, self.naver_news)

        next_page = response.css('div.paging a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
    
    def naver_news(self, response):
        item = NewscrawlerItem()
        
        title = response.css('div.article_info h3#articleTitle::text').get()
        url = response.url
        date = response.css('div.article_info span.t11::text').get().split(' ')[0]
        press = response.css('div.press_logo a img::attr(title)').get()
        #senti = response.css('a.u_likeit_button *::text').getall()
        #review = response.css('a#articleTitleCommentCount').getall()
        bodyList = response.css('div._article_body_contents *::text').getall()
        body = ''.join(bodyList).replace('  ','').replace('\t','').replace('\n','').replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}','')
        
        item['title'] = title
        item['url'] = url
        item['date'] = date
        item['press'] = press
        #item['senti'] = senti
        #item['review'] = review
        item['body'] = body
        
        yield item



