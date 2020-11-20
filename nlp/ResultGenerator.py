# generate word-cloud image

import numpy as np
from PIL import Image, ImageFont, ImageDraw
from wordcloud import WordCloud


class ResultGenerator:

    result_dir = './data/nlp/result/'

    @staticmethod
    def make_image(keywords, project_name):
        mask = np.array(Image.open(
            ResultGenerator.result_dir + project_name + '-mask.png'))

        wc = WordCloud(background_color="white",
                       max_words=1000,
                       mask=mask,
                       contour_width=3,
                       contour_color='black')

        # generate word cloud
        wc.generate_from_frequencies(keywords)
        wc.to_file(ResultGenerator.result_dir + project_name + '.png')
        wc.to_file('./docs/images/shapes/fullsize/' + project_name + '.png')

        # generate thumbnail
        image = Image.open(ResultGenerator.result_dir + project_name + '.png')
        size = image.size
        image.thumbnail((size[0] * 0.1, size[1] * 0.1),  Image.ANTIALIAS)
        image.save('./docs/images/shapes/thumbnails/' + project_name + '.png')

    # # redundant function?
    # @staticmethod
    # def getMaskTextColor(word,
    #                      font_size,
    #                      position,
    #                      orientation,
    #                      random_state=None,
    #                      **kwargs):
    #     return "hsl(0, 0%, 0%)"

    @staticmethod
    def make_mask(project_name):
        font_path = './data/Modak-Regular.ttf'
        project_name = project_name.upper()

        image = Image.new('RGB', (800, 800), (255, 255, 255))
        font = ImageFont.truetype(font_path, 900)
        draw = ImageDraw.Draw(image)

        size = draw.multiline_textsize(text=project_name, font=font, spacing=1)

        image = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(image)

        space_between_char = -80

        special_chars = ['a', 'v', 'm' ,'w' ,'o', 'q']
        reduced_space_chars = ['i']

        offset = -draw.textsize(
            text=project_name[0],
            font=font,
            spacing=1)[0] - space_between_char

        crop_right = 0
        crop_bottom = 0

        is_behind_reduced_space_char = False

        for char in project_name:
            text_size = draw.textsize(
                text=char,
                font=font,
                spacing=1)

            offset = text_size[0] + offset + space_between_char

            if is_behind_reduced_space_char:
                offset = offset + space_between_char*2

            if char.lower() in special_chars:
                offset = offset + space_between_char

            if char.lower() in reduced_space_chars:
                offset = offset - space_between_char*3
                is_behind_reduced_space_char = True
            else:
                is_behind_reduced_space_char = False

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
        # # (It will not change original image)
        # im1 = im.crop((left, top, right, bottom))

        image = image.crop((0, 0, crop_right, crop_bottom))

        image.save(ResultGenerator.result_dir + project_name.lower() + '-mask.png')
