import logging
import os

from gardiner2unicode import GardinerToUnicodeMap, UnicodeGlyphGenerator

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    g2u = GardinerToUnicodeMap()

    assert g2u.to_unicode_hex("A1") == "00013000"
    assert g2u.to_unicode_int("A1") == 77824
    assert g2u.to_unicode_char("A1") == "𓀀"

    # checking that every character in the Unicode block is present in the map
    for uid in range(int("13000", 16), int("1342F", 16)):
        unic = "000" + hex(uid)[2:].upper()
        if unic not in g2u.unicode2gardiner:
            raise Exception(f"Character {chr(uid)} ({unic}) was not found in the map!")

    os.makedirs("images", exist_ok=True)
    generator = UnicodeGlyphGenerator()

    for gardiner_code in g2u.gardiner2unicode:
        try:
            generator.generate_image(g2u.to_unicode_char(gardiner_code),
                                     save_path_png=f"images/{gardiner_code}.png")
        except Exception as e:
            print(gardiner_code, e)

    generator.generate_image(g2u.to_unicode_char("D20"), save_path_png="D20_image.png")
