# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import re

class VnexpressPipeline:

    def __init__(self):
        self.file = open('items2.csv', 'ab+')
        self.exporter = CsvItemExporter(self.file, 'unicode')
        self.exporter.start_exporting

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    
    def process_duplicate(self, item):
        link = item['link']

        # if link in self.seen:
        #     raise DropItem('Duplicate item %s' % link)
        
        self.seen.add(link)
    def pre_process(self, item):
        item['category'] = str(item['category'])
        item['date'] = str(item['date'])
        item['title'] = str(item['title'])
        item['body'] = str(item['body'])
        item['comment'] = str(item['comment'])
        item['link'] = str(item['link'])

        # get id user comment
        user = str(item['user'])
        user = str(re.findall(r'\d+', user))
        print (type(user))
        item['user'] = user

    def process_item(self, item, spider):
        self.pre_process(item)
        self.exporter.export_item(item)

        return item
