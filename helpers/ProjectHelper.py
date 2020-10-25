import os


class ProjectHelper:
    @staticmethod
    def getProjectName(fullUrl):
        result = ''

        nameSplitted = str.split(fullUrl, '/')
        if len(nameSplitted) > 2:
            # https://www.eclipse.org/paho/
            lastName = nameSplitted.pop()
            while lastName == '':
                lastName = nameSplitted.pop()
            result = lastName.lower()
        else:
            result = fullUrl.lower()

        # remove the 'iot'
        result = result.replace('iot', '').replace('.', ' ').strip()

        # remove the 'technology'
        result = result.replace('technology', '').replace('.', ' ').strip()

        # remove the 'tools'
        result = result.replace('tools', '').replace('.', ' ').strip()

        # handle special case
        if('agile' in result):
            result = 'agile'

        return result

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
