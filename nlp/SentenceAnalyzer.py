# Analyze linked sentences from Linker.py

import json
import os
from model.LinkKeyword import LinkKeyword, LinkKeywordEncoder, LinkProject
from model.GrammarRule import GrammarRule
from types import SimpleNamespace as Namespace

import nltk.tag, nltk.data
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

    path_to_grammar = './data/nlp/grammars.json'

    grammar_rules = []
    with open(path_to_grammar, 'r') as grammar_data:
        grammar_rules = json.load(grammar_data, object_hook=lambda d: Namespace(**d))

    standford_tagger = StanfordPOSTagger(path_to_tagger, path_to_jar)
    unified_tagger = nltk.data.load()

    for linked_keyword in linked_keywords:

        grammars = []

        for grammar in grammar_rules:
            grammar.set_keys(linked_keyword.Keys)
            grammars.append(grammar)

        for project in linked_keyword.projects:

            data_folder = './data/nlp/result/' + project.Project + "/"

            # create folder
            ProjectHelper.createDataFolder(data_folder)

            index = 1

            for sentence in project.Sentences:
                words = sentence.split()

                # TODO: add new tag for keyword
                tokens = standford_tagger.tag(words)
                grammar = convert_grammars(grammars)
                cp = RegexpParser(grammar)
                result = cp.parse(tokens)

                for chunk in result:
                    if type(chunk) is Tree:
                        for grammar in grammars:
                            if grammar.is_matched(chunk):
                                draw_tree(index, data_folder, chunk)
                                index = index + 1
