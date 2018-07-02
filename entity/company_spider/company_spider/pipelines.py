# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pandas as pd


class CompanySpiderPipeline(object):
    def process_item(self, item, spider):
        data = pd.DataFrame(item['data'], columns=item['cols'])
        file_name = item['title'][0] + '.csv'
        print(file_name)
        data.to_csv(file_name, sep=',', encoding='utf-8')
        return item
