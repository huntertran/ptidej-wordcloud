from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def loadRawDataFile():
    with open('./wordcloud/data/paho.txt', 'r', encoding="utf-8") as dataFile:
        return dataFile.readlines()


def combineStopwords():
    customizedStopwords = []
    with open('./nlp/customized_stopwords.txt', 'r', encoding='utf-8') as customizedStopwordsFile:
        customizedStopwords = customizedStopwordsFile.readlines()
        for index, word in enumerate(customizedStopwords):
            customizedStopwords[index] = word.strip('\r').strip('\n')
    
    combinedStopwords = stopwords.words('english')
    combinedStopwords.extend(customizedStopwords)

    dataLines = loadRawDataFile()
    keywords = []
    for line in dataLines:
        words = word_tokenize(line)

        for index, word in enumerate(words):
            words[index] = PorterStemmer().stem(word)

        keywords.extend([word for word in words if word not in combinedStopwords and word != '' and '//' not in word])
    
    keywords.sort()
    print(keywords)
