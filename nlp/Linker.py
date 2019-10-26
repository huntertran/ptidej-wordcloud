import json
from model.Site import Site
from model.SiteNode import SiteNode
from helpers.ProjectHelper import ProjectHelper

dataPath = './data/scrapy/'
defaultEncoding = 'utf-8'
resultedDataPath = './data/nlp/result/'


def create_link():
    projectNodes = []

    filePath = './data/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    index = 0
    for site in siteDataList:
        siteName = ProjectHelper.getProjectName(site.SiteUrl)
        # remove the 'iot'
        siteName = siteName.replace('iot','').replace('.',' ').strip()

        # handle special case
        if('agile' in siteName):
            siteName = 'agile'

        siteNode = SiteNode(index, siteName)

        projectNodes.append(siteNode)
        index += 1

    for siteNode in projectNodes:
        print(siteNode.key)
