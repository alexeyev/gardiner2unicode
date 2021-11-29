# coding: utf-8

import logging

from PIL import Image, ImageDraw, ImageFont


class UnicodeGlyphGenerator(object):

    def __init__(self, path_to_font: str = None, font_size: int = 72,
                 layout_engine=None, pixels_margin: int = 10, bkgr_color="#000000"):

        self.pixels_margin = pixels_margin
        self.bkgr_color = bkgr_color
        logging.debug("Reading fonts...")

        if path_to_font is None:

            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Trying backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources

            from . import data

            with pkg_resources.path(data, "NewGardinerSMP.ttf") as filepath:
                self.font = ImageFont.truetype(str(filepath), size=font_size, encoding="unic", layout_engine=layout_engine)
        else:
            self.font = ImageFont.truetype(path_to_font, size=font_size, encoding="unic", layout_engine=layout_engine)

    def generate_image(self, unicode_text: str, save_path_png=None):
        """
            Draws an image of the provided Unicode character using the font provided
            on construction of the `UnicodeGlyphGenerator` object
        :param unicode_text: a character to draw
        :param save_path_png: path for saving the PNG image
        """

        if len(unicode_text) > 1:
            logging.warning("Please not that the generated image might be formatted poorly "
                            "since you are trying to draw multiple signs.")

        text_width, text_height = self.font.getsize(unicode_text)
        canvas = Image.new("RGB", (text_width + self.pixels_margin, text_height + self.pixels_margin), (255, 255, 255))
        drawing_engine = ImageDraw.Draw(canvas)
        drawing_engine.text(xy=(self.pixels_margin // 2, self.pixels_margin // 2),
                            text=unicode_text, font=self.font, fill=self.bkgr_color)
        canvas.save(save_path_png, "PNG")