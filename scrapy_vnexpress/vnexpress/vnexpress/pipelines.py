# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from .items import CommentItem
import scrapy
import datetime 
from .items import UserItem

class VnexpressPipeline:

    def __init__(self):
        self.file = open('articles.csv','w+b')
        self.exporter = CsvItemExporter(self.file, 'unicode')
        self.exporter.fields_to_export = ['category', 'title', 'body', 'date', 'tags', 'link', 'articleID']
        self.exporter.start_exporting

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
class CommentPipeline:

    def __init__(self):
        self.file = open('comment_article.csv','w+b')
        self.exporter = CsvItemExporter(self.file, 'unicode')
        self.exporter.fields_to_export = ['articleID', 'userID', 'comment', 'userlike', 'time']
        self.exporter.start_exporting


    # def format_time(time):
    #     result =''
        
    #     return result

    def process_item(self, item, spider):
        print('this is comment pipeline \n\n')

        # format data to store in comment_article table
        format_item = Format_comment_item()

        if(item['total_comment'] !=0):
            total_comment = item['total_comment']
            for index in range(total_comment):
                format_item['articleID'] = item['articleID']
                # format_item['userID'] = int(item['all_comment'][index]['userid'])
                format_item['userID'] = item['all_comment'][index]['userid']
                format_item['comment'] = item['all_comment'][index]['content']
                format_item['userlike'] = item['all_comment'][index]['userlike']
                format_item['time'] = item['all_comment'][index]['time']
                print('this is from format item', format_item['userID'])
                self.exporter.export_item(format_item)
        return item

class Format_comment_item(scrapy.Item):
    articleID = scrapy.Field()
    userID = scrapy.Field()
    comment = scrapy.Field()
    userlike = scrapy.Field()
    time = scrapy.Field()
    pass

class UserPipeline:
    def __init__(self):
        self.file = open('user_comment.csv','w+b')
        self.exporter = CsvItemExporter(self.file, 'unicode')
        self.exporter.fields_to_export = ['userID', 'time', 'comment', 'url']
        # self.exporter.fields_to_export = ['userID', 'url', 'comment', 'articleID', 'categoryID']
        self.exporter.start_exporting
    
    def process_item(self, item, spider):
        
        print('process from pipeline ', len(item))
        try:
            for idx in range(5000):
                it = UserItem()
                it['userID'] = item['userID']
                it['time'] = item['time'][idx]
                it['comment'] = item['comment'][idx]
                it['url'] = item['url'][idx]
                self.exporter.export_item(it)
        except IndexError:
            return item
             
        return item
