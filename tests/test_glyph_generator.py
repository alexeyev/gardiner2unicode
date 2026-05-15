from PIL import Image

from gardiner2unicode import GardinerToUnicodeMap, UnicodeGlyphGenerator


def test_generate_image_returns_image_object():
    generator = UnicodeGlyphGenerator()
    image = generator.generate_image("𓀀")
    assert isinstance(image, Image.Image)
    assert image.size[0] > 0 and image.size[1] > 0


def test_generate_image_writes_png(tmp_path):
    generator = UnicodeGlyphGenerator()
    out = tmp_path / "A1.png"
    generator.generate_image("𓀀", save_path_png=str(out))
    assert out.exists() and out.stat().st_size > 0
    with Image.open(out) as written:
        assert written.format == "PNG"


def test_generate_image_for_every_code():
    """ Smoke test: rendering must not raise for any code in the map. """
    g2u = GardinerToUnicodeMap()
    generator = UnicodeGlyphGenerator()
    for code in list(g2u.gardiner2unicode)[:50]:
        image = generator.generate_image(g2u.to_unicode_char(code))
        assert isinstance(image, Image.Image)


def test_generator_accepts_fill_color_kwarg():
    # The kwarg was renamed from `bkgr_color` to `fill_color` in 1.0.0.
    generator = UnicodeGlyphGenerator(fill_color="#ff0000")
    assert generator.fill_color == "#ff0000"
