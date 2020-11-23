# Process crawled text to extract most popular words to generate word cloud

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import FreqDist
import re
from nlp.ResultGenerator import ResultGenerator
from helpers.ProjectHelper import ProjectHelper
from helpers.nlp_helper import combine_stopwords
from model.Site import StemmedWord

data_path = './data/scrapy/'
default_encoding = 'utf-8'
resulted_data_path = './data/nlp/result/'


def get_programming_language_list():
    programming_languages = []
    with open('./data/nlp/programming_languages.txt',
              'r',
              encoding=default_encoding) as programming_languages_file:
        lines = programming_languages_file.readlines()
        for line in lines:
            programming_languages.append(line.strip('\n'))
    return programming_languages


def is_match_special_string(word):
    match = re.search(r'\d*:', word)
    match_number = re.search(r'\d+', word)
    if match or match_number:
        return True
    else:
        return False


def insert_stemmed_keyword_with_un_stemmed_count(new_stemmed, new_un_stemmed, stemmed_word_list):
    is_existed = False
    for stemmed in stemmed_word_list:
        if stemmed.Text == new_stemmed:
            stemmed.addUnStemmed(new_un_stemmed)
            is_existed = True
            break

    if not is_existed:
        stemmed_word_list.append(StemmedWord(new_stemmed, new_un_stemmed))


def is_in_stopwords(stemmed_word, original_word, stopwords):
    return (stemmed_word not in stopwords
            and original_word.lower() not in stopwords
            and stemmed_word != ''
            and '//' not in stemmed_word
            and not is_match_special_string(stemmed_word))


def remove_stopwords(project_name, stopwords):
    data_lines = ProjectHelper.load_raw_data_file(project_name)
    keywords = []
    stemmed_keywords = []
    programming_language_keywords = []
    programming_languages = get_programming_language_list()

    stemmer = PorterStemmer()

    for line in data_lines:
        words = word_tokenize(line)
        for index, word in enumerate(words):
            words[index] = stemmer.stem(word)
            # check for stop words
            if is_in_stopwords(words[index], word, stopwords):
                if words[index] in programming_languages:
                    programming_language_keywords.append(words[index])
                else:
                    if words[index].lower() != project_name.lower():
                        keywords.append(words[index])
                        insert_stemmed_keyword_with_un_stemmed_count(words[index],
                                                                     word,
                                                                     stemmed_keywords)
    return programming_language_keywords, keywords, stemmed_keywords


def calculate_frequency_distribution(keywords, take_most=None):
    frequency_distribution = FreqDist(keywords)
    if take_most is not None:
        distribution_list = frequency_distribution.most_common(take_most)
    else:
        distribution_list = frequency_distribution.items()
    sorted_freq_dist = sorted(
        distribution_list,
        key=lambda kv: kv[1],
        reverse=True)
    return sorted_freq_dist


def calculate_frequency_distribution_from_stemmed_list(stemmed_word_list, take_most=None):
    sortedstemmed_word_list = sorted(
        stemmed_word_list,
        key=lambda kv: kv.count(),
        reverse=True)
    result = {}
    index = 0
    for stemmed_word in sortedstemmed_word_list:
        most_common_un_stemmed_word = stemmed_word.getMostCommonUnStemmed()
        result[most_common_un_stemmed_word] = stemmed_word.count()
        index += 1
        if take_most is not None and index >= take_most:
            break
    return result


def write_distribution_list_to_file(project_name, sorted_freq_dist,  suffix=None):
    ProjectHelper.create_data_folder(resulted_data_path)
    file_name_with_path = resulted_data_path + project_name
    if suffix is not None:
        file_name_with_path = file_name_with_path + '-' + suffix
    file_name_with_path = file_name_with_path + '.txt'
    with open(file_name_with_path, 'w+', encoding=default_encoding) as resultFile:
        for key in sorted_freq_dist:
            resultFile.writelines(
                key + ':' + str(sorted_freq_dist[key]) + '\n')


def generate_image_file(project_name, most_common_keywords):
    image_source = dict([keyword[0], keyword[1]]
                        for keyword in most_common_keywords)
    ResultGenerator.make_image(image_source, project_name)


def process(site_url):
    print('NLP Proccessing for ', site_url)
    project_name = ProjectHelper.get_project_name(site_url)
    stopwords = combine_stopwords()
    keywords_tuple = remove_stopwords(project_name, stopwords)

    # restore stem
    keywords = keywords_tuple[2]
    keywords_distribution = calculate_frequency_distribution_from_stemmed_list(
        keywords, 50)

    write_distribution_list_to_file(project_name, keywords_distribution)

    ResultGenerator.make_mask(project_name)
    ResultGenerator.make_image(keywords_distribution, project_name)
    print('Wordcloud generated for ', project_name)
