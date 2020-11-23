from nltk.corpus import stopwords

default_encoding = 'utf-8'


def combine_stopwords():
    customized_stopwords = []
    with open('./data/nlp/customized_stopwords.txt',
              'r',
              encoding=default_encoding) as customized_stopwords_file:
        customized_stopwords = customized_stopwords_file.readlines()
        for index, word in enumerate(customized_stopwords):
            customized_stopwords[index] = word.strip('\r').strip('\n')
    combined_stopwords = stopwords.words('english')
    combined_stopwords.extend(customized_stopwords)
    return combined_stopwords
