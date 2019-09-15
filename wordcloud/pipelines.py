# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class FileDictionary(object):
    def __init__(self, projectRoot, fileStream):
        self.projectRoot = projectRoot
        self.fileStream = fileStream

class WordcloudPipeline(object):
    # files = []

    # def open_spider(self, spider):
    #     for url in spider.urls:
            
    #         filePath = "./wordcloud/data/" + url + ".txt"
    #         projectFile = open(filePath,'w')

    #         fileDict = FileDictionary(url, projectFile)

    #         self.files.append(fileDict)

    # def close_spider(self, spider):
    #     for projectFile in self.files:
    #         projectFile.fileStream.close()

    def process_item(self, item, spider):
        # for fileDictItem in self.files:
        #     if fileDictItem.projectRoot == item.projectRoot:
        #         fileDictItem.projectFile.write(item.text + "\n")
        #         break
        return item
