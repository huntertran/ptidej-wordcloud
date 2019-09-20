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

    # @staticmethod
    # def class_mapper(d):
    #     return mapping[frozenset(d.keys())](**d)