# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os


class WordcloudPipeline(object):
    dataFolder = "./ptidejWordcloud/data/"

    def getProjectName(self, fullUrl):
        nameSplitted = str.split(fullUrl, '/')
        if len(nameSplitted) > 2:
            # https://www.eclipse.org/paho/
            return nameSplitted[3]
        else:
            return fullUrl

    def createDataFolder(self):
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)

    def open_spider(self, spider):
        # line = getattr(self, 'site_url', None)
        self.createDataFolder()
        line = spider.site_url
        if line is not None:
            projectName = self.getProjectName(line)
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
