import json
from model.Site import Site
from model.SiteNode import SiteNode
from helpers.ProjectHelper import ProjectHelper
from tabulate import tabulate
from nltk.tokenize import sent_tokenize
import pandas

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
    projectNames = []

    filePath = './data/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    index = 0
    for site in siteDataList:
        siteKey = getSiteKey(site.SiteUrl)

        # # TODO: REMOVE AFTER DEBUG
        # if(index > 5):
        #     break

        projectNodes[siteKey] = index
        projectNames.append(siteKey)
        index += 1

    print("End creating connected graph")

    # analyze
    index = 0
    dataFrame = pandas.DataFrame(columns=projectNames, index=projectNames)

    for site in siteDataList:

        # # TODO: REMOVE AFTER DEBUG
        # if(index > 5):
        #     break
        # else:
        #     index += 1

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

                        sorted_row_col = sort_num(col, row)
                        stringToAppend = ""
                        if pandas.isna(dataFrame.iloc[sorted_row_col[0], sorted_row_col[1]]):
                            dataFrame.iloc[sorted_row_col[0],
                                           sorted_row_col[1]] = ''
                            stringToAppend = sentence
                        else:
                            stringToAppend = dataFrame.iloc[sorted_row_col[0],
                                                            sorted_row_col[1]] + '\n' + sentence

                        dataFrame.iloc[sorted_row_col[0],
                                       sorted_row_col[1]] = stringToAppend

    dataFrame.to_csv('./data/nlp/connections.csv')
