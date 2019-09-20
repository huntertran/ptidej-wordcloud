import os

class ProjectHelper:
    @staticmethod
    def getProjectName(fullUrl):
        nameSplitted = str.split(fullUrl, '/')
        if len(nameSplitted) > 2:
            # https://www.eclipse.org/paho/
            return nameSplitted[3]
        else:
            return fullUrl

    @staticmethod
    def createDataFolder(folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)