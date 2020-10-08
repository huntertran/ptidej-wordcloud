# Analyze linked sentences from Linker.py

import json
import os
from model.LinkKeyword import LinkKeyword, LinkKeywordEncoder, LinkProject
from model.GrammarRule import GrammarRule
from types import SimpleNamespace as Namespace

import nltk.tag
import nltk.data
from nltk import pos_tag, RegexpParser
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tree import Tree
from nltk.draw.tree import TreeView
from nltk.tokenize import word_tokenize

from helpers.ProjectHelper import ProjectHelper
from helpers.nlp_helper import combineStopwords
from PIL import Image

linked_keywords = []

grammars = []


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r', encoding='utf8') as dataFile:
        return json.load(dataFile, object_hook=lambda d: Namespace(**d))


def draw_tree(index, rel, data_folder, result):
    ps_file = data_folder + str(index) + '_' + rel + '_output.ps'
    png_file = data_folder + str(index) + '_' + rel + '_output.png'

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


def modify_tag(keys, tokens):
    for num, token in enumerate(tokens):
        if token[0] in keys:
            tokens[num] = (token[0], 'KEYWORD')
    return tokens


def remove_sentence_splitter(tokens):
    return [token for token in tokens if token[0] not in [',',
                                                          ';',
                                                          ':',
                                                          '.',
                                                          '-']]


def parse_with_grammar(tagger, grammars, keys, sentence, index, data_folder):
    tokens = tagger.tag(word_tokenize(sentence))
    tokens = remove_sentence_splitter(tokens)
    tokens = modify_tag(keys, tokens)
    grammar = convert_grammars(grammars)
    cp = RegexpParser(grammar)
    result = cp.parse(tokens)
    for chunk in result:
        if type(chunk) is Tree:
            print('chunk found: ')
            print(chunk)
            for grammar in grammars:
                matched, rel = grammar.is_matched(chunk)
                if matched:
                    # chunk.draw()
                    print('MATCHED FOUND------------------------\n')
                    print(chunk)
                    print('-------------------------------------\n')
                    draw_tree(index, rel, data_folder, chunk)
                    index = index + 1


def start_analyze():
    linked_keywords = load_linked_result()

    # using the standford pos tagger for better result
    path_to_tagger = './standford_pos_tagger_data/english-bidirectional-distsim.tagger'
    path_to_jar = './standford_pos_tagger_data/stanford-postagger.jar'

    path_to_grammar = './data/nlp/grammars.json'

    grammar_rules = []
    with open(path_to_grammar, 'r') as grammar_data:
        grammar_rules = json.load(
            grammar_data, object_hook=lambda d: Namespace(**d))

    standford_tagger = StanfordPOSTagger(path_to_tagger, path_to_jar)

    # stopwords = combineStopwords()
    # stopwords.remove('use')

    for linked_keyword in linked_keywords:

        grammars = []

        for simple_namespace in grammar_rules:
            grammar = GrammarRule(simple_namespace.name,
                                  simple_namespace.grammar,
                                  linked_keyword.Keys,
                                  simple_namespace.key_position,
                                  simple_namespace.other_words,
                                  simple_namespace.other_words_position)
            grammar.set_keys(linked_keyword.Keys)
            grammars.append(grammar)

        for project in linked_keyword.projects:

            data_folder = './data/nlp/result/' + project.Project + "/"

            # create folder
            ProjectHelper.createDataFolder(data_folder)

            index = 1

            for sentence in project.Sentences:
                parse_with_grammar(standford_tagger,
                                   grammars,
                                   linked_keyword.Keys,
                                   sentence,
                                   index,
                                   data_folder)
