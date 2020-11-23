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

    def set_keys(self, keys):
        self.keys = keys

    def is_matched(self, tree):
        stemmer = PorterStemmer()

        if tree._label == self.name:
            # check key
            if tree[self.key_position][0] in self.keys:
                # TODO: fix for match wit new data structure
                # check other words
                stemmed = stemmer.stem(tree[self.other_words_position][0])
                for word_data in self.other_words:
                    if stemmed == word_data.word:
                        rel = word_data.relationship
                        return True, rel

        return False, ""


class OtherWord(object):
    def __init__(self, word=None, relationship=None):
        self.word = word
        self.relationship = relationship

    @staticmethod
    def decode_object(dict):
        return OtherWord(dict['word'], dict['relationship'])

    def is_matched(self, word_to_compare):
        return word_to_compare == self.word