# Analyze linked sentences from Linker.py

import json
import os
from model.LinkKeyword import LinkKeyword, LinkKeywordEncoder, LinkProject
from types import SimpleNamespace as Namespace
from nltk import pos_tag, RegexpParser

from nltk.tree import Tree
from nltk.draw.tree import TreeView

from helpers.ProjectHelper import ProjectHelper
from PIL import Image

linked_keywords = []


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r', encoding='utf8') as dataFile:
        return json.load(dataFile, object_hook=lambda d: Namespace(**d))


def start_analyze():
    linked_keywords = load_linked_result()
    for linked_keyword in linked_keywords:
        for project in linked_keyword.projects:

            data_folder = './data/nlp/result/' + project.Project + "/"

            # create folder
            ProjectHelper.createDataFolder(data_folder)

            index = 1

            for sentence in project.Sentences:
                words = sentence.split()
                tokens = pos_tag(words)
                grammar = """
                        implement_keyword: {<VB><NNP>}
                        implementation_of_keyword: {<NP|NNP|NN><IN><NNP>}
                        support_keyword_protocol: {<VB><NNP><NN>}
                        """
                cp = RegexpParser(grammar)
                result = cp.parse(tokens)

                ps_file = data_folder + str(index) + '_output.ps'
                png_file = data_folder + str(index) + '_output.png'

                TreeView(result)._cframe.print_to_file(ps_file)
                
                # # convert ps to png
                im = Image.open(ps_file)
                fig = im.convert('RGBA')
                fig.save(png_file, lossless = True)

                # print(result)
                index = index + 1
