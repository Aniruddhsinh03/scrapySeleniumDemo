# -*- coding: utf-8 -*-
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyseleniumdemoPipeline:
    def process_item(self, item, spider):
        os.chdir('E:\IMAGE STORE')
        # rename image with title
        if item['images'][0]['path']:
            new_image_name = item['title'][0] + '.jpg'
            new_image_path = 'full/' + new_image_name

            os.rename(item['images'][0]['path'], new_image_path)
