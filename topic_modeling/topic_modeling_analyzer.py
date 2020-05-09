import os.path
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt

from helpers.nlp_helper import combineStopwords
from helpers.ProjectHelper import ProjectHelper


def preprocess_data(paragraphs):
    stopwords = combineStopwords()
    stemmer = PorterStemmer()

    texts = []

    for paragraph in paragraphs:
        # clean and tokenize document string
        raw = paragraph.lower()
        words = word_tokenize(paragraph)
        # remove stopwords
        stopped_tokens = [i for i in words if not i in stopwords]
        # stem tokens
        stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]

        texts.append(stemmed_tokens)
    
    return texts


def start_topic_modeling(project_name):
    print("Latent Sematic Indexing for ", project_name)
    paragraphs = ProjectHelper.load_raw_data_file(project_name)
    preprocess_data(paragraphs)