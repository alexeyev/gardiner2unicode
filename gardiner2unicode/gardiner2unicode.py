# coding: utf-8

import re
import logging
from functools import lru_cache
from typing import Optional, Dict

import wikitextparser as wtp

_TAG_PATTERN = re.compile("<[^>]*>")


def _strip_tags(string: str) -> str:
    """ Removing everything in the form '<...>'."""
    return re.sub(_TAG_PATTERN, "", string)


def _map(text_data: str) -> Dict[str, str]:
    """ Parsing the table from https://en.wikipedia.org/w/index.php?title=Template:List_of_hieroglyphs&action=edit """

    parsing_result = wtp.parse(text_data)

    # a list of dicts of potentially useful info
    data = []

    for t in parsing_result.templates:

        # potentially useful headers
        curr_data = {"gardiner": None, "description": None, "pron": None, "notes": None,
                     "unicode": None, "unicode_id": None, "meanings": []}

        # if there is no 'gardiner' column, we should not use the current row
        gardiner_met = False

        for arg in t.arguments:
            if arg.name == "H":
                # unicode symbol of interest
                curr_data["unicode"] = arg.value.strip()
            elif arg.name.startswith("t"):
                curr_data["meanings"].append(arg.value.strip())
            elif arg.name == "desc":
                curr_data["description"] = arg.value.strip()
            elif arg.name == "gardiner":
                # Gardiner's code of interest
                gardiner_met = True
                curr_data["gardiner"] = _strip_tags(arg.value).strip()
            elif arg.name == "unicode":
                # unicode table cell ID
                curr_data["unicode_id"] = arg.value.strip()
            elif arg.name == "pron":
                # pronunciation
                curr_data["pron"] = arg.value.strip()
            elif arg.name == "notes":
                curr_data["notes"] = arg.value.strip()
            elif arg.name != "1" and not arg.name == "2" \
                    and not arg.name == "date" \
                    and not arg.name == "qid" \
                    and not arg.name == "reason" \
                    and not arg.name == "url" and not arg.name == "website" and not arg.name == "title":
                raise Exception(f"Unknown field: [{arg.name.strip()}] arg_value = {arg.value}")

        # if information of interest is not present in the current row, we skip it
        if not gardiner_met or (curr_data.get("unicode", None) is None and curr_data["unicode_id"] is None):
            t = str(t).replace("\n", " ")
            logging.debug(f"This line does not contain any Gardiner code! {t}")
        else:
            data.append(curr_data)

    result = {}

    for dictionary in data:
        # converting codes to the 8-character form e.g. "00013000"
        eight_letter_unicode = dictionary["unicode_id"].zfill(8)
        result[dictionary["gardiner"]] = eight_letter_unicode  # , dictionary["unicode"])

    return result


class GardinerToUnicodeMap(object):

    def __init__(self, path: str = None):

        logging.debug("Parsing \"Template:List_of_hieroglyphs\"...")

        if path is None:
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Trying backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources

            from . import data

            with pkg_resources.path(data, "wikipedia_table.wiki") as filepath:
                raw_text = open(filepath, "r+", encoding="utf-8").read().strip()
        else:
            raw_text = open(path, "r+", encoding="utf-8").read().strip()

        self.gardiner2unicode = _map(raw_text)
        self.unicode2gardiner = {v: k for k, v in self.gardiner2unicode.items()}

        # checking if the mapping is a bijection
        assert len(self.gardiner2unicode) == len(self.unicode2gardiner)

        logging.debug(f"Table parsed successfully. Map of size [{len(self.gardiner2unicode)}] was built.")

    @lru_cache(maxsize=10000)
    def to_unicode_hex(self, code: str) -> Optional[str]:
        """
            Returns an 8-digit hex number of the corresponding
            Unicode character, e.g. "A1" -> "00013000"
        """
        return self.gardiner2unicode.get(code, None)

    @lru_cache(maxsize=10000)
    def to_unicode_int(self, code: str) -> Optional[int]:
        """
            Returns an integer number of the corresponding
            Unicode character, e.g. "A1" -> 77824
        """
        hx = self.to_unicode_hex(code)
        return int(hx, 16) if hx is not None else None

    @lru_cache(maxsize=10000)
    def to_unicode_char(self, code: str) -> Optional[int]:
        """
            Returns the corresponding Unicode character, e.g. "A1" -> "𓀀"
        """
        hx = self.to_unicode_hex(code)
        return chr(int(hx, 16)) if hx is not None else None

    @lru_cache(maxsize=10000)
    def to_gardiner_from_hex(self, hex: str) -> Optional[str]:
        """
            Returns a Gardiner code of the corresponding
            Unicode character having the given hex number,
            e.g. "00013000" -> "A1"
        """
        return self.unicode2gardiner.get(hex.upper(), None)

    @lru_cache(maxsize=10000)
    def to_gardiner_from_int(self, unicode_decimal_number: int) -> Optional[str]:
        """
            Returns a Gardiner code of the corresponding
            Unicode character having the given number,
            e.g. 77824 -> "A1"
        """
        hex_code = "000" + hex(unicode_decimal_number)[2:].upper()
        return self.to_gardiner_from_hex(hex_code)

    @lru_cache(maxsize=10000)
    def to_gardiner_from_chr(self, char: str) -> Optional[str]:
        """
            Returns a Gardiner code of the corresponding
            Unicode character, e.g. "𓀀" -> "A1"
        """
        assert len(char) == 1
        hex_code = "000" + hex(ord(char))[2:].upper()
        return self.to_gardiner_from_hex(hex_code)
