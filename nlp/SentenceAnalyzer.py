# Analyze linked sentences from Linker.py

import json
import os
from model.LinkKeyword import LinkKeyword, LinkKeywordEncoder, LinkProject
from model.GrammarRule import GrammarRule
from types import SimpleNamespace as Namespace
from nltk import pos_tag, RegexpParser
from nltk.tag.stanford import StanfordPOSTagger

from nltk.tree import Tree
from nltk.draw.tree import TreeView

from helpers.ProjectHelper import ProjectHelper
from PIL import Image

linked_keywords = []

grammars = []


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r', encoding='utf8') as dataFile:
        return json.load(dataFile, object_hook=lambda d: Namespace(**d))


def draw_tree(index, data_folder, result):
    ps_file = data_folder + str(index) + '_output.ps'
    png_file = data_folder + str(index) + '_output.png'

    TreeView(result)._cframe.print_to_file(ps_file)

    # # convert ps to png
    im = Image.open(ps_file)
    fig = im.convert('RGBA')
    fig.save(png_file, lossless=True)


def convert_grammars(grammars):
    result = ""
    for grammar in grammars:
        result = result + '\n' + grammar.name + ": " + grammar.grammar

    return result


def start_analyze():
    linked_keywords = load_linked_result()

    # using the standford pos tagger for better result
    path_to_tagger = './standford_pos_tagger_data/english-bidirectional-distsim.tagger'
    path_to_jar = './standford_pos_tagger_data/stanford-postagger.jar'

    standford_tagger = StanfordPOSTagger(path_to_tagger, path_to_jar)

    for linked_keyword in linked_keywords:
        
        grammars.append(GrammarRule("implement_keyword",
                                    "{<VB><NNP>}",
                                    linked_keyword.Keys,
                                    1,
                                    ["implement"],
                                    0))
        grammars.append(GrammarRule("implementation_of_keyword",
                                    "{<NP|NNP|NN|NNS><IN><DT>?<NNP>}",
                                    linked_keyword.Keys,
                                    2,
                                    ["implement"],
                                    0))
        grammars.append(GrammarRule("support_keyword_protocol",
                                    "{<VB><NNP><NN>}",
                                    linked_keyword.Keys,
                                    1,
                                    ["support", "use"],
                                    0))
        for project in linked_keyword.projects:

            data_folder = './data/nlp/result/' + project.Project + "/"

            # create folder
            ProjectHelper.createDataFolder(data_folder)

            index = 1

            for sentence in project.Sentences:
                words = sentence.split()
                tokens = standford_tagger.tag(words)
                # grammar = """
                #         implement_keyword: {<VB><NNP>}
                #         implementation_of_keyword: {<NP|NNP|NN|NNS><IN><NNP>}
                #         support_keyword_protocol: {<VB><NNP><NN>}
                #         """
                grammar = convert_grammars(grammars)
                cp = RegexpParser(grammar)
                result = cp.parse(tokens)

                for chunk in result:
                    if type(chunk) is Tree:
                        for grammar in grammars:
                            if grammar.is_matched(chunk):
                                draw_tree(index, data_folder, chunk)
                                index = index + 1
