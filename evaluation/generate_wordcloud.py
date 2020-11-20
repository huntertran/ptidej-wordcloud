from wordcloud import WordCloud

data_file = './evaluation/data.txt'
result_file = './evaluation/result.png'

keywords = {}

with open(data_file, 'r', encoding='utf-8') as lines:
    for line in lines:
        key = line.split(':')[0]
        value = line.split(':')[1].rstrip()

        keywords[key] = float(value)

wc = WordCloud(background_color='white',
               max_words=1000,
               contour_width=3,
               contour_color='black')

wc.generate_from_frequencies(keywords)
wc.to_file(result_file)
