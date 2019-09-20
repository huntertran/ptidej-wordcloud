import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class ResultGenerator:

    @staticmethod
    def makeImage(keywords, projectName):
        # alice_mask = np.array(Image.open("alice_mask.png"))

        # wc = WordCloud(background_color="white", max_words=1000, mask=alice_mask)
        wc = WordCloud(background_color="white", max_words=1000)
        # generate word cloud
        wc.generate_from_frequencies(keywords)

        # show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('./nlp/data/' + projectName + '.png')