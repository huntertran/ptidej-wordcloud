from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk import pos_tag
import os
import collections
from nltk.stem import WordNetLemmatizer
from nlp.model.keyword import Keyword


def loadRawDataFile():
    with open('./wordcloud/data/paho.txt', 'r', encoding="utf-8") as dataFile:
        return dataFile.readlines()

def createDataFolder():
    if not os.path.exists('./nlp/data/'):
        os.makedirs('./nlp/data/')

def getProgrammingLanguageList():
    programmingLanguages = []
    with open('./nlp/programming_languages.txt','r',encoding='utf-8') as programmingLanguagesFile:
        lines = programmingLanguagesFile.readlines()
        for line in lines:
            programmingLanguages.append(line.strip('\n'))

    return programmingLanguages

def combineStopwords():
    programmingLanguages = getProgrammingLanguageList()

    customizedStopwords = []

    with open('./nlp/customized_stopwords.txt', 'r', encoding='utf-8') as customizedStopwordsFile:
        customizedStopwords = customizedStopwordsFile.readlines()
        for index, word in enumerate(customizedStopwords):
            customizedStopwords[index] = word.strip('\r').strip('\n')
    
    combinedStopwords = stopwords.words('english')
    combinedStopwords.extend(customizedStopwords)

    dataLines = loadRawDataFile()
    keywords = []
    programmingLanguageKeywords = []
    for line in dataLines:
        words = word_tokenize(line)

        for index, word in enumerate(words):
            # words[index] = SnowballStemmer('english').stem(word)
            words[index] = PorterStemmer().stem(word)

            # check for stop words
            if words[index] not in combinedStopwords and words[index] != '' and '//' not in words[index]:
                if words[index] in programmingLanguages:
                    programmingLanguageKeywords.append(words[index])
                else:
                    keywords.append(words[index])


        # keywords.extend([word for word in words if word not in combinedStopwords and word != '' and '//' not in word])
    # lemmatizer = WordNetLemmatizer()
    # with open('./nlp/programming_language_lemma.txt','r',encoding='utf-8') as programmingLanguageLemmaFile:
    #     lines = programmingLanguageLemmaFile.readlines()
    #     for line in lines:
    #         lemmatizer.lemmatize(line.strip('\n'),'pl')
    
    # programmingLanguageKeywords = lemmatizer.lemmatize()

    fd = FreqDist(keywords)
    plfd = FreqDist(programmingLanguageKeywords)

    # result = []
    # for word in fd.items():
    #     result.append(Keyword(word[0], word[1]))

    sortedFreqDist = sorted(fd.items(), key=lambda kv:kv[1], reverse=True)
    sortedProgrammingLanguagesFreqDist = sorted(plfd.items(), key=lambda kv:kv[1], reverse=True)

    createDataFolder()
    with open('./nlp/data/paho.txt','w+',encoding='utf-8') as resultFile:
        for key, value in sortedFreqDist:
            resultFile.writelines(key + ':' + str(value) + '\n')

    with open('./nlp/data/paho-programmingLanguages.txt','w+',encoding='utf-8') as resultFile:
        for key, value in sortedProgrammingLanguagesFreqDist:
            resultFile.writelines(key + ':' + str(value) + '\n')
        # resultFile.write(','.join(fd.items()))

    # print(fd.most_common(100))
    # fd.plot()
    
    # keywords.sort()
    # print(keywords)
