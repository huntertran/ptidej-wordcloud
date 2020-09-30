# Analyze linked sentences from Linker.py

import json
from model.LinkKeyword import LinkKeyword, LinkKeywordEncoder, LinkProject
from types import SimpleNamespace as Namespace
from nltk import pos_tag, RegexpParser

linked_keywords = []


def load_linked_result():
    file_path = './data/linked.json'
    with open(file_path, 'r') as dataFile:
        return json.load(dataFile, object_hook=lambda d: Namespace(**d))


def start_analyze():
    linked_keywords = load_linked_result()
    for linked_keyword in linked_keywords:
        for project in linked_keyword.projects:
            for sentence in project.Sentences:
                words = sentence.split()
                tokens = pos_tag(words)
                grammar = "NP: {<VB>?<NNP>?}"
                cp = RegexpParser(grammar)
                result = cp.parse(tokens)
                print(result)
