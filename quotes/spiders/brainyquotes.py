# -*- coding: utf-8 -*-
import json

import scrapy

class BrainyquotesSpider(scrapy.Spider):
    name = 'brainyquotes'
    allowed_domains = ['www.brainyquote.com']

    def __init__(self, topic=None, *args, **kwargs):
        super(BrainyquotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.brainyquote.com/topics/%s' % topic]

    def start_requests(self):
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):


        '''This will extract all cards which initially contains our     
           quote'''

        #cards = response.xpath('//*[@id=""]/div')
        #print(cards[0].xpath('//div/div/a[1]/text()'))
        '''we will loop through cards to extract all the quotes'''

        #print(response.xpath('//*[@id="quotesList"]/div[1]/div[1]/div[1]/div[1]/a/text()').getall())
        for quote in response.xpath('//div[@id="quotesList"]/div'):
            text=quote.xpath('div/div[1]/div/a/text()').get()
            author=quote.xpath('div/div[1]/div/div/a/text()').get()
            tags=quote.xpath('div/div[3]/div/a/text()').getall()
            if(not len(tags)):
                tags = quote.xpath('div[2]/div/a/text()').getall()
            if(text=='\n' or author==None):
                continue
            yield {
                'text': text,
                'author': author,
                'topic': response.xpath('//h1/text()').get().split()[0],
                'from': self.name,
                'tags':tags
            }

