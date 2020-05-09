import os


class ProjectHelper:
    @staticmethod
    def getProjectName(fullUrl):
        nameSplitted = str.split(fullUrl, '/')
        if len(nameSplitted) > 2:
            # https://www.eclipse.org/paho/
            lastName = nameSplitted.pop()
            while lastName is '':
                lastName = nameSplitted.pop()
            return lastName
        else:
            return fullUrl

    @staticmethod
    def createDataFolder(folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

    @staticmethod
    def load_raw_data_file(project_name):
        dataPath = './data/scrapy/'
        defaultEncoding = 'utf-8'
        with open(dataPath + project_name + '.txt', 'r', encoding=defaultEncoding) as dataFile:
            return dataFile.readlines()
