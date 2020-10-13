import json

from types import SimpleNamespace as Namespace

from nltk.tag.stanford import StanfordPOSTagger

from model.GrammarRule import GrammarRule
from helpers.nlp_helper import combineStopwords
from helpers.ProjectHelper import ProjectHelper
from nlp.SentenceAnalyzer import load_linked_result, parse_with_grammar


def start_analyze_test():
    # using the standford pos tagger for better result
    path_to_tagger = './standford_pos_tagger_data/english-bidirectional-distsim.tagger'
    path_to_jar = './standford_pos_tagger_data/stanford-postagger.jar'

    path_to_grammar = './data/nlp/grammars.json'

    grammar_rules = []
    with open(path_to_grammar, 'r') as grammar_data:
        grammar_rules = json.load(
            grammar_data, object_hook=lambda d: Namespace(**d))

    standford_tagger = StanfordPOSTagger(path_to_tagger, path_to_jar)

    stopwords = combineStopwords()
    stopwords.remove('use')

    grammars = []

    keys = ['WoT']

    for simple_namespace in grammar_rules:
        grammar = GrammarRule(simple_namespace.name,
                              simple_namespace.grammar,
                              keys,
                              simple_namespace.key_position,
                              simple_namespace.other_words,
                              simple_namespace.other_words_position)
        # grammar.set_keys(linked_keyword.Keys)
        grammars.append(grammar)

    data_folder = './data/nlp/result/test/'
    ProjectHelper.createDataFolder(data_folder)

    parse_with_grammar(standford_tagger,
                       grammars,
                       keys,
                       'node-wot is the official reference implementation of the W3C WoT Working Group and implements the so-called \"Servient Architecture\":',
                       1,
                       data_folder)
