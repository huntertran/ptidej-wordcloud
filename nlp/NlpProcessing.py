# Process crawled text to extract most popular words to generate word cloud


from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk import pos_tag
import os
import re
import collections
from nltk.stem import WordNetLemmatizer
from nlp.ResultGenerator import ResultGenerator
from helpers.ProjectHelper import ProjectHelper
from helpers.nlp_helper import combineStopwords
from model.Site import StemmedWord

dataPath = './data/scrapy/'
defaultEncoding = 'utf-8'
resultedDataPath = './data/nlp/result/'


def getProgrammingLanguageList():
    programmingLanguages = []
    with open('./data/nlp/programming_languages.txt',
              'r',
              encoding=defaultEncoding) as programmingLanguagesFile:
        lines = programmingLanguagesFile.readlines()
        for line in lines:
            programmingLanguages.append(line.strip('\n'))
    return programmingLanguages


# def combineStopwords(projectName):
#     customizedStopwords = []
#     with open('./data/nlp/customized_stopwords.txt',
#               'r',
#               encoding=defaultEncoding) as customizedStopwordsFile:
#         customizedStopwords = customizedStopwordsFile.readlines()
#         for index, word in enumerate(customizedStopwords):
#             customizedStopwords[index] = word.strip('\r').strip('\n')
#     combinedStopwords = stopwords.words('english')
#     combinedStopwords.extend(customizedStopwords)
#     return combinedStopwords


def isMatchSpecialString(word):
    match = re.search(r'\d*:', word)
    matchNumber = re.search(r'\d+', word)
    if match or matchNumber:
        return True
    else:
        return False


def insertStemmedKeywordWithUnStemmedCount(newStemmed, newUnStemmed, stemmedWordList):
    isExisted = False
    for stemmed in stemmedWordList:
        if stemmed.Text == newStemmed:
            stemmed.addUnStemmed(newUnStemmed)
            isExisted = True
            break

    if not isExisted:
        stemmedWordList.append(StemmedWord(newStemmed, newUnStemmed))


def isInStopwords(stemmedWord, originalWord, stopwords):
    return (stemmedWord not in stopwords
            and originalWord.lower() not in stopwords
            and stemmedWord != ''
            and '//' not in stemmedWord
            and not isMatchSpecialString(stemmedWord))


def removeStopwords(projectName, stopwords):
    dataLines = ProjectHelper.load_raw_data_file(projectName)
    keywords = []
    stemmedKeywords = []
    programmingLanguageKeywords = []
    programmingLanguages = getProgrammingLanguageList()

    stemmer = PorterStemmer()

    for line in dataLines:
        words = word_tokenize(line)
        for index, word in enumerate(words):
            # words[index] = SnowballStemmer('english').stem(word)
            words[index] = stemmer.stem(word)
            # check for stop words
            if isInStopwords(words[index], word, stopwords):
                if words[index] in programmingLanguages:
                    programmingLanguageKeywords.append(words[index])
                else:
                    if words[index].lower() != projectName.lower():
                        keywords.append(words[index])
                        insertStemmedKeywordWithUnStemmedCount(
                            words[index], word, stemmedKeywords)
    return programmingLanguageKeywords, keywords, stemmedKeywords


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


def calculateFrequencyDistributionFromStemmedList(stemmedWordList, takeMost=None):
    sortedStemmedWordList = sorted(
        stemmedWordList,
        key=lambda kv: kv.count(),
        reverse=True)
    result = {}
    index = 0
    for stemmedWord in sortedStemmedWordList:
        mostCommonUnStemmedWord = stemmedWord.getMostCommonUnStemmed()
        result[mostCommonUnStemmedWord] = stemmedWord.count()
        index += 1
        if takeMost is not None and index >= takeMost:
            break
    return result


def writeDistributionListToFile(projectName, sortedFreqDist,  suffix=None):
    ProjectHelper.createDataFolder(resultedDataPath)
    fileNameWithPath = resultedDataPath + projectName
    if suffix is not None:
        fileNameWithPath = fileNameWithPath + '-' + suffix
    fileNameWithPath = fileNameWithPath + '.txt'
    with open(fileNameWithPath, 'w+', encoding=defaultEncoding) as resultFile:
        for key in sortedFreqDist:
            resultFile.writelines(key + ':' + str(sortedFreqDist[key]) + '\n')


def generateImageFile(projectName, mostCommonKeywords):
    imageSource = dict([keyword[0], keyword[1]]
                       for keyword in mostCommonKeywords)
    ResultGenerator.makeImage(imageSource, projectName)


def process(siteUrl):
    print('NLP Proccessing for ', siteUrl)
    projectName = ProjectHelper.getProjectName(siteUrl)
    stopwords = combineStopwords()
    keywordsTuple = removeStopwords(projectName, stopwords)

    # keywords
    # keywords = keywordsTuple[1]
    # keywordsDistribution = calculateFrequencyDistribution(keywords, 50)

    # restore stem
    keywords = keywordsTuple[2]
    keywordsDistribution = calculateFrequencyDistributionFromStemmedList(
        keywords, 50)

    writeDistributionListToFile(projectName, keywordsDistribution)

    ResultGenerator.makeMask(projectName)
    ResultGenerator.makeImage(keywordsDistribution, projectName)
    print('Wordcloud generated for ', projectName)
