# -*- coding: utf-8 -*-
import scrapy
import csv

class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads'
    page_number = 2
    curr_topic = ""
    allowed_domains = ['goodreads.com']
    
    def __init__(self, topic=None, *args, **kwargs):
        super(GoodreadsSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.goodreads.com/quotes/tag/%s?page=1' % topic]
        self.curr_topic = topic

    #csvFile = open('quotes.csv','a',encoding='utf-8')
    #csvWriter = csv.writer(csvFile)
    #csvWriter.writerow(['source', 'title', 'length', 'author', 'likes', 'tags'])

    def parse(self, response):

        all_div_quotes = response.css('div.quoteDetails')

        for quotes in all_div_quotes:
            quote_title = quotes.css('div.quoteText::text').extract()
            quote_author = quotes.css('div.quoteText span::text').extract()

            quote_tags = quotes.css(
                'div.quoteFooter div.greyText.smallText.left a::text').extract()

            title_trim_newLine = quote_title[0].replace('\n', '')
            title = title_trim_newLine.strip('\"')

            author_trim_comma = quote_author[0].replace(',', '')
            author = author_trim_comma.replace('\n', '')

            yield {'text':title, 'author': author, 'topic':self.curr_topic, 'from': self.name,'tags':quote_tags}

            #GoodreadsSpider.csvWriter.writerow([source, title, len(quote_title[0]), author, likes[0], quote_tags[0]])

        sources = [self.curr_topic]

        for source in sources:

            next_page = 'https://www.goodreads.com/quotes/tag/{}?page='.format(source) + str(GoodreadsSpider.page_number)
            if GoodreadsSpider.page_number < 10:
        	    GoodreadsSpider.page_number += 1
        	    yield response.follow(next_page, callback=self.parse)
        


