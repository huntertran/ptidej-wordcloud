# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from helpers.ProjectHelper import ProjectHelper

class WordcloudPipeline(object):
    dataFolder = "./ptidejWordcloud/data/"

    def open_spider(self, spider):
        ProjectHelper.createDataFolder(self.dataFolder)
        siteUrl = spider.siteUrl
        if siteUrl is not None:
            projectName = ProjectHelper.getProjectName(siteUrl)
            filePath = self.dataFolder + projectName + ".txt"
            self.outputFile = open(filePath, 'w+', encoding='utf-8')

    def close_spider(self, spider):
        self.outputFile.close()

    def process_item(self, item, spider):
        text = item['t']
        if not 'function' in text and not '\n' in text:
            if not '\t' in text:
                self.outputFile.write(text + "\n")
        return item
