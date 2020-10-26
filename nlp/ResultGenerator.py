# generate word-cloud image

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class ResultGenerator:

    @staticmethod
    def makeImage(keywords, projectName):
        mask = np.array(Image.open(
            './data/nlp/result/' + projectName + '-mask.png'))

        wc = WordCloud(background_color="white",
                       max_words=1000,
                       mask=mask,
                       contour_width=3,
                       contour_color='black')

        # generate word cloud
        wc.generate_from_frequencies(keywords)
        wc.to_file('./data/nlp/result/' + projectName + '.png')
        wc.to_file('./docs/images/shapes/fullsize/' + projectName + '.png')

        # generate thumbnail
        image = Image.open('./data/nlp/result/' + projectName + '.png')
        size = image.size
        image.thumbnail((size[0] * 0.1, size[1] * 0.1),  Image.ANTIALIAS)
        image.save('./docs/images/shapes/thumbnails/' + projectName + '.png')

    @staticmethod
    def getMaskTextColor(word,
                         font_size,
                         position,
                         orientation,
                         random_state=None,
                         **kwargs):
        return "hsl(0, 0%, 0%)"

    @staticmethod
    def makeMask(projectName):
        font_path = './data/Modak-Regular.ttf'
        projectName = projectName.upper()

        image = Image.new('RGB', (800, 800), (255, 255, 255))
        font = ImageFont.truetype(font_path, 900)
        draw = ImageDraw.Draw(image)

        size = draw.multiline_textsize(text=projectName, font=font, spacing=1)

        image = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(image)

        spaceBetweenChar = -80

        specialChars = ['a', 'v', 'w', 'm']
        reducedSpaceChars = ['i']

        offset = -draw.textsize(
            text=projectName[0],
            font=font,
            spacing=1)[0] - spaceBetweenChar

        crop_right = 0
        crop_bottom = 0

        for char in projectName:
            text_size = draw.textsize(
                text=char,
                font=font,
                spacing=1)

            offset = text_size[0] + offset + spaceBetweenChar

            if char.lower() in specialChars:
                offset = offset + spaceBetweenChar

            if char.lower() in reducedSpaceChars:
                offset = offset - spaceBetweenChar*3

            draw.multiline_text(
                xy=(offset, -300),
                text=char,
                font=font,
                spacing=1,
                align="left",
                fill=(0, 0, 0))

            crop_bottom = text_size[1] - 280
            crop_right = text_size[0] + offset

        # # Setting the points for cropped image
        # left = 5
        # top = height / 4
        # right = 164
        # bottom = 3 * height / 4

        # # Cropped image of above dimension
        # # (It will not change orginal image)
        # im1 = im.crop((left, top, right, bottom))

        image = image.crop((0, 0, crop_right, crop_bottom))

        image.save('./data/nlp/result/' + projectName.lower() + '-mask.png')
