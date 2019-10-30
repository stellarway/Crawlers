# -*- coding: utf-8 -*-
import scrapy


class OlivebestSpider(scrapy.Spider):
    name = 'OliveBest'
    allowed_domains = ['www.oliveyoung.co.kr']
    start_urls = []
    codes=['10000010001','10000010002','10000010003','10000010004','10000010005','10000010006','10000010007',
    '10000020001','10000020002','10000020003','10000030002','10000030003','10000030004']
    for CatNo in codes:
        start_urls.append('http://www.oliveyoung.co.kr/store/main/getBestList.do?fltDispCatNo={}'.format(CatNo))
    def parse(self, response):
        pass
