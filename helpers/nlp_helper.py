from nltk.corpus import stopwords

defaultEncoding = 'utf-8'


def combine_stopwords():
    customized_stopwords = []
    with open('./data/nlp/customized_stopwords.txt',
              'r',
              encoding=defaultEncoding) as customizedStopwordsFile:
        customized_stopwords = customizedStopwordsFile.readlines()
        for index, word in enumerate(customized_stopwords):
            customized_stopwords[index] = word.strip('\r').strip('\n')
    combined_stopwords = stopwords.words('english')
    combined_stopwords.extend(customized_stopwords)
    return combined_stopwords
