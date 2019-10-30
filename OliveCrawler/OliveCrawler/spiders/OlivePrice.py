# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import os

class OlivepriceSpider(scrapy.Spider):
    name = 'OlivePrice'
    start_urls=[]
    colnames=['addInfoNm', 'brndNm', 'dispRegDate', 'gdasCont','goodsNm','goodsNo','mbrNo','star'] 
    result = pd.read_csv('./review.csv', names=colnames, header=None)
    goodsNo = list(result.goodsNo[:-1])
    for num in goodsNo:
        url = 'http://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo={}'.format(num)
        start_urls.append(url)

    def parse(self, response):
        yield {
            'goodsNo': response.url.split('=')[-1],
            'price': response.css('ul.info_list span.tx_num::text').get().replace(',',''),
            'img_url': response.css('div.prd_img img::attr(src)').get()}