import json
from model.Site import Site
from model.SiteNode import SiteNode
from helpers.ProjectHelper import ProjectHelper

dataPath = './data/scrapy/'
defaultEncoding = 'utf-8'
resultedDataPath = './data/nlp/result/'


def print_graph(relationships, siteNodes):
    # print headers
    print('', end='\t', flush=True)
    for node in siteNodes:
        print(node.key, end='\t', flush=True)
    print('\n')

    index = 0
    for row in relationships:
        print(siteNodes[index].key, end='\t', flush=True)

        for col in row:
            print(col, end='\t', flush=True)
        
        print('\n')
        index += 1



def create_link():
    projectNodes = []
    relationships = []

    filePath = './data/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    index = 0
    for site in siteDataList:
        siteName = ProjectHelper.getProjectName(site.SiteUrl)
        # remove the 'iot'
        siteName = siteName.replace('iot', '').replace('.', ' ').strip()

        # handle special case
        if('agile' in siteName):
            siteName = 'agile'

        siteNode = SiteNode(index, siteName)

        # TODO: REMOVE AFTER DEBUG
        if(index > 5):
            break

        projectNodes.append(siteNode)
        index += 1

    for siteNode in projectNodes:
        print(siteNode.key)
        relationships.append([0] * len(projectNodes))

    print("End creating connected graph")

    print_graph(relationships, projectNodes)
