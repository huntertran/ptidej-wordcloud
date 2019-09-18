from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
import os
import collections


def loadRawDataFile():
    with open('./wordcloud/data/paho.txt', 'r', encoding="utf-8") as dataFile:
        return dataFile.readlines()

def createDataFolder():
    if not os.path.exists('./nlp/data/'):
        os.makedirs('./nlp/data/')

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
            # words[index] = SnowballStemmer('english').stem(word)
            words[index] = PorterStemmer().stem(word)


        keywords.extend([word for word in words if word not in combinedStopwords and word != '' and '//' not in word])

    fd = FreqDist(keywords)
    sortedFreqDist = sorted(fd.items(), key=lambda kv:kv[1], reverse=True)

    createDataFolder()
    with open('./nlp/data/paho.txt','w+',encoding='utf-8') as resultFile:
        for key, value in sortedFreqDist:
            resultFile.writelines(key + ':' + str(value) + '\n')
        # resultFile.write(','.join(fd.items()))

    # print(fd.most_common(100))
    # fd.plot()
    
    # keywords.sort()
    # print(keywords)
