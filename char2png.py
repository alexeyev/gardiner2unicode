# # coding: utf-8
# from PIL import Image, ImageDraw, ImageFont
#
# # sample text and font
# unicode_text = u"Unicode Characters: \u00C6 \u00E6 \u00B2 \u00C4 \u00D1 \u220F 𓀀"
# verdana_font = ImageFont.truetype("DejaVuSans.ttf", 20, encoding="unic")
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

# save the blank canvas to a file
canvas.save("unicode-text.png", "PNG")
