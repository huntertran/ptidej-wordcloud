# find text link between projects

import json
import jsonpickle

from model.Site import Site
from model.LinkKeyword import LinkKeyword, LinkProject
from helpers.ProjectHelper import ProjectHelper

from tabulate import tabulate
from nltk.tokenize import sent_tokenize

dataPath = './data/scrapy/'
defaultEncoding = 'utf-8'
resultedDataPath = './data/nlp/result/'


def print_graph(relationships, site_nodes):
    project_keys = []
    for node in site_nodes:
        project_keys.append(node)

    print(tabulate(relationships,
                   headers=project_keys,
                   showindex=project_keys,
                   tablefmt='fancy_grid'))


def get_link_keyword():
    with open('./data/nlp/link_keyword.json', 'r') as data:
        link_keyword = json.load(
            data, object_hook=LinkKeyword.decode_object)
    return link_keyword


def sort_num(first, second):
    if(first > second):
        return second, first
    else:
        return first, second


def add_linked_sentence(link_keyword, sentences, project_name):

    link_project = LinkProject(project_name)
    for key in link_keyword.Keys:
        for sentence in sentences:
            if key in sentence:
                link_project.add_sentence(sentence)

    return link_project


def analyze_site(site, link_keywords):
    # # TODO: REMOVE AFTER DEBUG
    # if(index > 5):
    #     break
    # else:
    #     index += 1

    project_name = ProjectHelper.get_project_name(site.site_url)

    text_lines = ProjectHelper.load_raw_data_file(project_name)

    for text_line in text_lines:
        sentences = sent_tokenize(text_line)

        for link_keyword in link_keywords:
            link_project = add_linked_sentence(
                link_keyword, sentences, project_name)
            if link_project.sentences is not None and len(link_project.sentences) > 0:
                link_keyword.add_link_project(link_project)


def create_link():
    project_nodes = {}
    project_names = []
    link_keywords = []

    file_path = './data/sitelist.json'

    with open(file_path, 'r') as dataFile:
        site_data_list = json.load(dataFile, object_hook=Site.decode_object)

    link_keywords = get_link_keyword()

    # create barebone connected graph
    index = 0
    for site in site_data_list:
        project_name = ProjectHelper.get_project_name(site.site_url)

        # # TODO: REMOVE AFTER DEBUG
        # if(index > 5):
        #     break

        project_nodes[project_name] = index
        project_names.append(project_name)
        index += 1

    print("End creating connected graph")

    for site in site_data_list:
        print("Analyzing site: " + site.site_url)
        analyze_site(site, link_keywords)

    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)

    with open('./data/linked.json', 'w', encoding='utf8') as dataFile:
        dataFile.write(jsonpickle.encode(link_keywords))

    print("Data wrote to linked.json")
