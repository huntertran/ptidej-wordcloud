from nltk.corpus import stopwords


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
    for line in dataLines:
        words = line.lower().split()
        temp = [word for word in words if word not in combinedStopwords and word != '']
        print(temp)
