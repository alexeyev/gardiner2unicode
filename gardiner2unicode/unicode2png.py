import logging
from importlib.resources import files
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


class UnicodeGlyphGenerator:

    def __init__(self, path_to_font: str = None, font_size: int = 72,
                 layout_engine=None, pixels_margin: int = 10, fill_color="#000000"):

        self.pixels_margin = pixels_margin
        self.fill_color = fill_color
        logging.debug("Reading fonts...")

        if path_to_font is None:
            from . import data
            with files(data).joinpath("NewGardinerSMP.ttf").open("rb") as font_file:
                self.font = ImageFont.truetype(font_file, size=font_size,
                                               encoding="unic", layout_engine=layout_engine)
        else:
            self.font = ImageFont.truetype(path_to_font, size=font_size,
                                           encoding="unic", layout_engine=layout_engine)

    def generate_image(self, unicode_text: str, save_path_png: Optional[str] = None) -> Image.Image:
        """
            Draws an image of the provided Unicode character using the font provided
            on construction of the `UnicodeGlyphGenerator` object.

        :param unicode_text: a character to draw
        :param save_path_png: optional path for saving the PNG image
        :return: the rendered PIL.Image.Image object
        """

        if len(unicode_text) > 1:
            logging.warning("Please note that the generated image might be formatted poorly "
                            "since you are trying to draw multiple signs.")

        # `ImageFont.getsize` was deprecated in Pillow 9.2.0 and removed in Pillow 10.0.0;
        # `getbbox` returns (left, top, right, bottom) and is the supported replacement.
        left, top, right, bottom = self.font.getbbox(unicode_text)
        text_width, text_height = right - left, bottom - top

        canvas = Image.new("RGB",
                           (text_width + self.pixels_margin, text_height + self.pixels_margin),
                           (255, 255, 255))
        drawing_engine = ImageDraw.Draw(canvas)
        drawing_engine.text(xy=(self.pixels_margin // 2 - left, self.pixels_margin // 2 - top),
                            text=unicode_text, font=self.font, fill=self.fill_color)

        if save_path_png is not None:
            canvas.save(save_path_png, "PNG")

        return canvas
