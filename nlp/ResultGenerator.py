import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class ResultGenerator:

    @staticmethod
    def makeImage(keywords, projectName):
        mask = np.array(Image.open(
            './data/nlp/result/' + projectName + '-mask.png'))

        wc = WordCloud(background_color="white", max_words=1000,
                       mask=mask, contour_width=3, contour_color='black')
        # generate word cloud
        wc.generate_from_frequencies(keywords)
        wc.to_file('./data/nlp/result/' + projectName + '.png')

        # plt.imshow(wc, interpolation="bilinear")
        # plt.axis("off")
        # plt.savefig('./data/nlp/result/' + projectName + '.png')

    @staticmethod
    def getMaskTextColor(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%, 0%)"

    @staticmethod
    def makeMask(projectName):
        font_path = './data/Modak-Regular.ttf'

        image = Image.new('RGB', (800, 800), (255, 255, 255))
        font = ImageFont.truetype(font_path, 900)
        draw = ImageDraw.Draw(image)

        size = draw.multiline_textsize(text=projectName, font=font, spacing=1)

        image = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(image)

        spaceBetweenChar = -80

        specialChars = ['a', 'v']
        reducedSpaceChars = ['i']

        offset = -draw.textsize(
            text=projectName[0],
            font=font, spacing=1)[0] - spaceBetweenChar

        for char in projectName:
            offset = draw.textsize(
                text=char,
                font=font,
                spacing=1)[0] + offset + spaceBetweenChar

            if char.lower() in specialChars:
                offset = offset + spaceBetweenChar

            if char.lower() in reducedSpaceChars:
                offset = offset - spaceBetweenChar*3

            draw.multiline_text(
                xy=(offset, -100),
                text=char,
                font=font,
                spacing=1,
                align="left",
                fill=(0, 0, 0))

            if char.lower() in reducedSpaceChars:
                offset = offset + spaceBetweenChar*3

        image.save('./data/nlp/result/' + projectName.lower() + '-mask.png')
