# Analyze linked sentences from Linker.py

import json
import jsonpickle

from model.GrammarRule import GrammarRule
from types import SimpleNamespace as Namespace

from nltk import RegexpParser
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tree import Tree
# from nltk.draw.tree import TreeView
from nltk.tokenize import word_tokenize

from helpers.ProjectHelper import ProjectHelper
from PIL import Image

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

linked_keywords = []
grammars = []


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r', encoding='utf8') as data_file:
        return jsonpickle.decode(data_file.read())


def save_linked_result(link_keywords):
    with open('./data/linked.json', 'w', encoding='utf8') as data_file:
        data_file.write(jsonpickle.encode(link_keywords))


def load_grammar_rules(path_to_grammar):
    with open(path_to_grammar, 'r') as grammar_data:
        return json.load(grammar_data, object_hook=lambda d: Namespace(**d))


# def draw_tree(index, rel, data_folder, result):
#     ps_file = data_folder + str(index) + '_' + rel + '_output.ps'
#     png_file = data_folder + str(index) + '_' + rel + '_output.png'

#     TreeView(result)._cframe.print_to_file(ps_file)

#     # convert ps to png
#     im = Image.open(ps_file)
#     fig = im.convert('RGBA')
#     fig.save(png_file, lossless=True)


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


def transform_keys_in_sentence(keys, sentence):
    for key in keys:
        if ' ' in key:
            sentence = sentence.replace(key, key.replace(' ', ''))

    return sentence


def transform_keys(keys):
    for num, key in enumerate(keys):
        if ' ' in key:
            keys[num] = key.replace(' ', '')

    return keys


def remove_sentence_splitter(tokens):
    return [token for token in tokens if token[0] not in [',',
                                                          ';',
                                                          ':',
                                                          '.',
                                                          '-']]


def parse_with_grammar(tagger, grammars, keys, sentence, index, data_folder):
    sentence = transform_keys_in_sentence(keys, sentence)
    keys = transform_keys(keys)
    tokens = []

    try:
        tokens = tagger.tag(word_tokenize(sentence))
    except OSError:
        return []

    tokens = remove_sentence_splitter(tokens)
    tokens = modify_tag(keys, tokens)
    grammar = convert_grammars(grammars)
    cp = RegexpParser(grammar)
    parsed_token = cp.parse(tokens)

    relationships = add_matched_chunk_to_relationships(parsed_token, index)

    return relationships

def add_matched_chunk_to_relationships(parsed_tokens, index):
    relationships = []

    for chunk in parsed_tokens:
        if type(chunk) is Tree:
            # print('chunk found: ')
            # print(chunk)
            for grammar in grammars:
                matched, rel = grammar.is_matched(chunk)
                if matched:
                    # chunk.draw()
                    # print('MATCHED FOUND------------------------\n')
                    # print(chunk)
                    # print('-------------------------------------\n')
                    # draw_tree(index, rel, data_folder, chunk)
                    if rel not in relationships:
                        relationships.append(rel)
                    index = index + 1

    return relationships

def append_unique_relationships(project, standford_tagger, linked_keyword, index, data_folder):

    relationships = []

    for sentence in project.Sentences:

        # try encode with ascii to eliminate usage of utf-16
        encoded = sentence.encode('ascii', 'replace').decode()
        if '?' in encoded:
            sentence = encoded

        sentence_relationships = parse_with_grammar(standford_tagger,
                                                    grammars,
                                                    linked_keyword.Keys,
                                                    sentence,
                                                    index,
                                                    data_folder)
        for rel in sentence_relationships:
            if rel not in relationships:
                relationships.append(rel)
                print("New relationship founded: " + sentence)

    return relationships


def start_analyze():
    linked_keywords = load_linked_result()

    # using the standford pos tagger for better result
    path_to_tagger = './standford_pos_tagger_data/english-bidirectional-distsim.tagger'
    path_to_jar = './standford_pos_tagger_data/stanford-postagger.jar'

    path_to_grammar = './data/nlp/grammars.json'

    grammar_rules = load_grammar_rules(path_to_grammar)

    standford_tagger = StanfordPOSTagger(path_to_tagger, path_to_jar)

    print("Start keyword analysis")

    for linked_keyword in linked_keywords:

        print("Start analyzing keyword: " + linked_keyword.Description)

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

            print("Analyzing project: " + project.Project)

            data_folder = './data/nlp/result/' + project.Project + "/"

            # create folder
            ProjectHelper.create_data_folder(data_folder)

            index = 1

            relationships = append_unique_relationships(project, standford_tagger, linked_keyword, index, data_folder)

            project.add_relationships(relationships)

    save_linked_result(linked_keywords)
