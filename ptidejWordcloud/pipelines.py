# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from helpers.ProjectHelper import ProjectHelper

class WordcloudPipeline(object):
    data_folder = "./data/scrapy/"

    def open_spider(self, spider):
        ProjectHelper.create_data_folder(self.data_folder)
        site_url = spider.siteUrl
        if site_url is not None:
            project_name = ProjectHelper.get_project_name(site_url)
            file_path = self.data_folder + project_name + ".txt"
            self.output_file = open(file_path, 'w+', encoding='utf-8')

    def close_spider(self, spider):
        self.output_file.close()

    def process_item(self, item, spider):
        text = item['t']
        if not 'function' in text and not '\n' in text and not '\t' in text:
            self.output_file.write(text + "\n")
        return item
