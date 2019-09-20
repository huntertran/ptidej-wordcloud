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
from nlp.ResultGenerator import ResultGenerator
from helpers.ProjectHelper import ProjectHelper

dataPath = './ptidejWordcloud/data/'
defaultEncoding = 'utf-8'
resultedDataPath = './nlp/data/'


def loadRawDataFile(projectName):
    with open(dataPath + projectName + '.txt', 'r', encoding=defaultEncoding) as dataFile:
        return dataFile.readlines()


def createDataFolder():
    if not os.path.exists(resultedDataPath):
        os.makedirs(resultedDataPath)


def getProgrammingLanguageList():
    programmingLanguages = []
    with open('./nlp/programming_languages.txt', 'r', encoding=defaultEncoding) as programmingLanguagesFile:
        lines = programmingLanguagesFile.readlines()
        for line in lines:
            programmingLanguages.append(line.strip('\n'))
    return programmingLanguages


def combineStopwords(projectName):
    customizedStopwords = []
    with open('./nlp/customized_stopwords.txt', 'r', encoding=defaultEncoding) as customizedStopwordsFile:
        customizedStopwords = customizedStopwordsFile.readlines()
        for index, word in enumerate(customizedStopwords):
            customizedStopwords[index] = word.strip('\r').strip('\n')
    combinedStopwords = stopwords.words('english')
    combinedStopwords.extend(customizedStopwords)
    return combinedStopwords


def removeStopwords(projectName, stopwords):
    dataLines = loadRawDataFile(projectName)
    keywords = []
    programmingLanguageKeywords = []
    for line in dataLines:
        words = word_tokenize(line)
        for index, word in enumerate(words):
            # words[index] = SnowballStemmer('english').stem(word)
            words[index] = PorterStemmer().stem(word)
            # check for stop words
            programmingLanguages = getProgrammingLanguageList()
            if words[index] not in stopwords and words[index] != '' and '//' not in words[index]:
                if words[index] in programmingLanguages:
                    programmingLanguageKeywords.append(words[index])
                else:
                    keywords.append(words[index])
    return programmingLanguageKeywords, keywords


def calculateFrequencyDistribution(keywords, takeMost=None):
    frequencyDistribution = FreqDist(keywords)
    if takeMost is not None:
        distributionList = frequencyDistribution.most_common(takeMost)
    else:
        distributionList = frequencyDistribution.items()
    sortedFreqDist = sorted(
        distributionList,
        key=lambda kv: kv[1],
        reverse=True)
    return sortedFreqDist


def writeDistributionListToFile(projectName, sortedFreqDist,  suffix=None):
    fileNameWithPath = resultedDataPath + projectName
    if suffix is not None:
        fileNameWithPath = fileNameWithPath + '-' + suffix
    fileNameWithPath = fileNameWithPath + '.txt'
    with open(fileNameWithPath, 'w+', encoding=defaultEncoding) as resultFile:
        for key, value in sortedFreqDist:
            resultFile.writelines(key + ':' + str(value) + '\n')


def generateImageFile(projectName, mostCommonKeywords):
    imageSource = dict([keyword[0], keyword[1]]
                       for keyword in mostCommonKeywords)
    ResultGenerator.makeImage(imageSource, projectName)


def process(siteUrl):
    projectName = ProjectHelper.getProjectName(siteUrl)
    stopwords = combineStopwords(projectName)
    keywordsTuple = removeStopwords(projectName, stopwords)
    # keywords
    keywords = keywordsTuple[1]
    keywordsDistribution = calculateFrequencyDistribution(keywords, 50)
    writeDistributionListToFile(projectName, keywordsDistribution)
    generateImageFile(projectName, keywordsDistribution)