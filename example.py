# coding: utf-8

from gardiner2unicode import GardinerToUnicodeMap
import logging

if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    g2u = GardinerToUnicodeMap()

    assert g2u.to_unicode_hex("A1") == "00013000"
    assert g2u.to_unicode_int("A1") == 77824

    # checking if all the characters available in Unicode table
    # can be found in the map
    for uid in range(int("13000", 16), int("1342F", 16)):
        unic = "000" + hex(uid)[2:].upper()
        if unic not in g2u.unicode2gardiner:
            raise Exception(f"Character {chr(uid)} ({unic}) was not found in the map!")
