# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Mp3DownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    movie_name = scrapy.Field()
    stars = scrapy.Field()
    music = scrapy.Field()
    director = scrapy.Field()
    link = scrapy.Field()
