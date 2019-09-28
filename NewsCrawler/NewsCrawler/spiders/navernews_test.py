# -*- coding: utf-8 -*-
import scrapy
from dateutil.relativedelta import relativedelta
from datetime import date
import pandas as pd
from NewsCrawler.items import NewscrawlerItem
from urllib import parse
import requests
import re

class NavernewsSpider(scrapy.Spider):
    name = 'navernews_test'

    start_urls=['https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=030&aid=0002701982',
    'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=015&aid=0004051001',
    'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=417&aid=0000367689',
    'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=030&aid=0002786131',
    'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=293&aid=0000021695',
    'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=277&aid=0004526338']

               
    def parse(self, response):
        item = NewscrawlerItem()
        # basic information
        title = response.css('div.article_info h3#articleTitle::text').get()
        url = response.url
        date = response.css('div.article_info span.t11::text').get().split(' ')[0]
        press = response.css('div.press_logo a img::attr(title)').get()
        bodyList = response.css('div._article_body_contents *::text').getall()
        tempbody = ''.join(bodyList)
        
        pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+.*)|  |\t|\n|\xa0'
        body = re.sub(pattern, '', tempbody).replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}','')
        # sentimental infomation
        pick_binary = response.css('div.head_channel::attr(style)').get()
        pick = 0 if 'none' in pick_binary else 1

        _url = parse.parse_qs(parse.urlsplit(response.url).query)
        oid = _url['oid'][0]
        aid = _url['aid'][0]

        react_url = 'https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&q=NEWS%5Bne_{0}_{1}%5D%7CNEWS_SUMMARY%5B{0}_{1}%5D%7CNEWS_MAIN%5Bne_{0}_{1}%5D&isDuplication=false'.format(oid,aid)
        react_resp=requests.get(react_url)
        react_json = react_resp.json()['contents'][0]['reactions']
        react = {}
        for i in range(len(react_json)):
            react[react_json[i]['reactionType']]=react_json[i]['count']
        recommend_json = react_resp.json()['contents'][2]['reactions']
        recommend = recommend_json[0]['count'] if recommend_json else 0

        comment_url = 'https://news.naver.com/api/comment/listCount.json?resultType=MAP&ticket=news&lang=ko&country=KR&objectId=news{0},{1}'.format(oid,aid)
        comment_resp = requests.get(comment_url)
        comment_json = comment_resp.json()['result']
        comment = list(comment_json.values())[0]['comment']

        # wrapping
        item['title'] = title
        item['url'] = url
        item['date'] = date
        item['press'] = press
        item['body'] = body
        item['pick'] = pick
        item['react'] = react
        item['comment'] = comment
        item['recommend'] = recommend
        
        yield item



