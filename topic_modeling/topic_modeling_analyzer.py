import os.path
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer, word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt

from helpers.nlp_helper import combineStopwords
from helpers.ProjectHelper import ProjectHelper


def preprocess_data(paragraphs):
    pos_tags = []
    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph)
        sentences = [word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        print(sentences)


def start_topic_modeling(project_name):
    print("Latent Sematic Indexing for ", project_name)
    paragraphs = ProjectHelper.load_raw_data_file(project_name)
    preprocess_data(paragraphs)