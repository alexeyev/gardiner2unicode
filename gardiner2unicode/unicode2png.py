# coding: utf-8
from PIL import Image, ImageDraw, ImageFont

class UnicodeGlyphGenerator(object):

    pass


# # sample text and font
# unicode_text = u"\U00013000 \U0001342b"
#
# # seguihis should be available on Windows
# verdana_font = ImageFont.truetype("seguihis.ttf", 72, encoding="unic")
#
# # get the line size
# text_width, text_height = verdana_font.getsize(unicode_text)
#
# # create a blank canvas with extra space between lines
# canvas = Image.new('RGB', (text_width + 10, text_height + 10), (255, 255, 255))
#
# # draw the text onto the text canvas, and use black as the text color
# draw = ImageDraw.Draw(canvas)
# draw.text((5, 5), unicode_text, font=verdana_font, fill="#000000")
# 
# # save the blank canvas to a file
# canvas.save("unicode-text.png", "PNG")
