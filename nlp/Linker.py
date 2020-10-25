# find text link between projects

import json
import pandas
import jsonpickle

from model.Site import Site
from model.SiteNode import SiteNode
from model.LinkKeyword import LinkKeyword, LinkKeywordEncoder, LinkProject
from helpers.ProjectHelper import ProjectHelper

from tabulate import tabulate
from nltk.tokenize import sent_tokenize

dataPath = './data/scrapy/'
defaultEncoding = 'utf-8'
resultedDataPath = './data/nlp/result/'


def print_graph(relationships, siteNodes):
    projectKeys = []
    for node in siteNodes:
        projectKeys.append(node)

    print(tabulate(relationships,
                   headers=projectKeys,
                   showindex=projectKeys,
                   tablefmt='fancy_grid'))


# def getSiteKey(siteUrl):
#     siteName = ProjectHelper.getProjectName(siteUrl)
#     # remove the 'iot'
#     siteName = siteName.replace('iot', '').replace('.', ' ').strip()

#     # handle special case
#     if('agile' in siteName):
#         siteName = 'agile'

#     return siteName


def get_link_keyword():
    with open('./data/nlp/link_keyword.json', 'r') as data:
        link_keyword = json.load(
            data, object_hook=LinkKeyword.decode_LinkKeyword)
    return link_keyword


def sort_num(first, second):
    if(first > second):
        return second, first
    else:
        return first, second


def analyze_site(site, link_keywords):
    # # TODO: REMOVE AFTER DEBUG
    # if(index > 5):
    #     break
    # else:
    #     index += 1

    project_name = ProjectHelper.getProjectName(site.SiteUrl)
    # siteKey = ProjectHelper.getProjectName(site.SiteUrl)

    textLines = ProjectHelper.load_raw_data_file(project_name)

    for textLine in textLines:
        sentences = sent_tokenize(textLine)

        for link_keyword in link_keywords:
            link_project = LinkProject(project_name)
            for key in link_keyword.Keys:
                for sentence in sentences:
                    if key in sentence:
                        link_project.add_sentence(sentence)
            if link_project.Sentences is not None and len(link_project.Sentences) > 0:
                link_keyword.add_link_project(link_project)


def create_link():
    projectNodes = {}
    relationships = []
    projectNames = []
    link_keywords = []

    filePath = './data/sitelist.json'

    with open(filePath, 'r') as dataFile:
        siteDataList = json.load(dataFile, object_hook=Site.decode_Site)

    link_keywords = get_link_keyword()

    # create barebone connected graph
    index = 0
    for site in siteDataList:
        project_name = ProjectHelper.getProjectName(site.SiteUrl)

        # # TODO: REMOVE AFTER DEBUG
        # if(index > 5):
        #     break

        projectNodes[project_name] = index
        projectNames.append(project_name)
        index += 1

    print("End creating connected graph")

    for site in siteDataList:
        analyze_site(site, link_keywords)

    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    # json_text = jsonpickle.encode(link_keywords)

    with open('./data/linked.json', 'w', encoding='utf8') as dataFile:
        dataFile.write(jsonpickle.encode(link_keywords))

    # with open('./data/linked.json', 'w', encoding='utf8') as dataFile:
    #     json.dump(link_keywords, dataFile, cls=LinkKeywordEncoder, indent=4, ensure_ascii=False)
