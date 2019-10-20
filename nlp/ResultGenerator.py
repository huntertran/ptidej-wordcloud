import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class ResultGenerator:

    @staticmethod
    def makeImage(keywords, projectName):
        mask = np.array(Image.open('./data/nlp/result/' + projectName + '-mask.png'))

        wc = WordCloud(background_color="white", max_words=1000, mask=mask, contour_width=3, contour_color='black')
        # generate word cloud
        wc.generate_from_frequencies(keywords)

        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('./data/nlp/result/' + projectName + '.png')

    @staticmethod
    def getMaskTextColor(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%, 0%)"

    @staticmethod
    def makeMask(projectName):
        wc = WordCloud(background_color="white", max_words=1, scale=4, color_func=ResultGenerator.getMaskTextColor)
        wc.generate(projectName)
        wc.to_file('./data/nlp/result/' + projectName + '-mask.png')

        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

        # plt.savefig('./data/nlp/result/' + projectName + '-mask.png')