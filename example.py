# coding: utf-8

from gardiner2unicode import GardinerToUnicodeMap

if __name__ == "__main__":

    g2u = GardinerToUnicodeMap()
    print(g2u.gardiner2unicode)
    print(g2u.to_unicode_hex("A1"))
    print(g2u.to_unicode_int("A1"))