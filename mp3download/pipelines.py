# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class Mp3DownloadPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect("movies_link.db")
        self.curr = self.conn.cursor()

    def store_db(self, item):
        self.curr.execute("""insert into movie_data (movie_name,stars,music,director,link,info)values (?,?,?,?,?,
        "default")""", (
            item['movie_name'],
            item['stars'],
            item['music'],
            item['director'],
            item['link'],
        ))

        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
