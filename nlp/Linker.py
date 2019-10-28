import json
from model.Site import Site
from model.SiteNode import SiteNode
from helpers.ProjectHelper import ProjectHelper
from tabulate import tabulate
from nltk.tokenize import sent_tokenize

dataPath = './data/scrapy/'
defaultEncoding = 'utf-8'
resultedDataPath = './data/nlp/result/'


def loadRawDataFile(projectName):
    with open(dataPath + projectName + '.txt', 'r', encoding=defaultEncoding) as dataFile:
        return dataFile.readlines()


def print_graph(relationships, siteNodes):
    projectKeys = []
    for node in siteNodes:
        projectKeys.append(node)

    print(tabulate(relationships,
                   headers=projectKeys,
                   showindex=projectKeys,
                   tablefmt='fancy_grid'))


def getSiteKey(siteUrl):
    siteName = ProjectHelper.getProjectName(siteUrl)
    # remove the 'iot'
    siteName = siteName.replace('iot', '').replace('.', ' ').strip()

    # handle special case
    if('agile' in siteName):
        siteName = 'agile'

    return siteName


def sort_num(first, second):
    if(first > second):
        return second, first
    else:
        return first, second


def create_link():
    projectNodes = {}
    relationships = []

    filePath = './data/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    index = 0
    for site in siteDataList:
        siteKey = getSiteKey(site.SiteUrl)
        # siteNode = SiteNode(index, siteKey)
        # siteNode = {siteKey: index}

        # TODO: REMOVE AFTER DEBUG
        if(index > 5):
            break

        # projectNodes.update({siteKey: index})
        projectNodes[siteKey] = index
        index += 1

    for siteNode in projectNodes:
        relationships.append([[]] * len(projectNodes))

    print("End creating connected graph")

    print_graph(relationships, projectNodes)

    # analyze
    index = 0

    for site in siteDataList:

        # TODO: REMOVE AFTER DEBUG
        if(index > 5):
            break
        else:
            index += 1

        projectName = ProjectHelper.getProjectName(site.SiteUrl)
        siteKey = getSiteKey(site.SiteUrl)

        textLines = loadRawDataFile(projectName)

        for textLine in textLines:
            sentences = sent_tokenize(textLine)

            for sentence in sentences:
                for node in projectNodes:
                    if(node == siteKey):
                        continue

                    if node in sentence:
                        row = projectNodes[node]
                        col = projectNodes.get(siteKey)
                        # relationships[row][col].append(sentence)
                        # old_list = relationships[row][col]
                        # old_list.append(1)
                        # print(old_list)

                        sorted_row_col = sort_num(row, col)

                        relationships[sorted_row_col[0]][sorted_row_col[1]] = 1

    print_graph(relationships, projectNodes)
