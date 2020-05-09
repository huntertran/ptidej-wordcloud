from nltk.corpus import stopwords


defaultEncoding = 'utf-8'

def combineStopwords():
    customizedStopwords = []
    with open('./data/nlp/customized_stopwords.txt',
              'r',
              encoding=defaultEncoding) as customizedStopwordsFile:
        customizedStopwords = customizedStopwordsFile.readlines()
        for index, word in enumerate(customizedStopwords):
            customizedStopwords[index] = word.strip('\r').strip('\n')
    combinedStopwords = stopwords.words('english')
    combinedStopwords.extend(customizedStopwords)
    return combinedStopwords