# model for rule set

from nltk import PorterStemmer

class GrammarRule(object):
    def __init__(self,
                 name=None,
                 grammar=None,
                 keys=None,
                 key_position=None,
                 other_words=None,
                 other_words_position=None):
        self.name = name
        self.grammar = grammar
        self.keys = keys
        self.key_position = key_position
        self.other_words = other_words
        self.other_words_position = other_words_position

    def is_matched(self, tree):
        stemmer = PorterStemmer()

        if tree._label == self.name:
            # check key
            if tree[self.key_position][0] in self.keys:
                # check other words
                if stemmer.stem(tree[self.other_words_position][0]) in self.other_words:
                    return True

        return False

class OtherWord(object):
    def __init__(self, word=None, relationship=None):
        self.word = word
        self.relationship = relationship

    
