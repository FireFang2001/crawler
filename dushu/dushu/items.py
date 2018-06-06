# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    auther = scrapy.Field()
    publisher = scrapy.Field()
    price = scrapy.Field()
    book_desc = scrapy.Field()
    auther_desc = scrapy.Field()
    contents = scrapy.Field()
