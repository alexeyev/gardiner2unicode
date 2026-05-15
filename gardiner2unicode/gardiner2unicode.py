import logging
import re
from importlib.resources import files
from typing import Optional

import wikitextparser as wtp

_TAG_PATTERN = re.compile("<[^>]*>")

# Argument names that may appear in the Wikipedia template but carry no
# information we need; anything outside this set raises, so that upstream
# template changes are noticed instead of silently ignored.
_IGNORED_ARGS = {"1", "2", "date", "qid", "reason", "url", "website", "title"}


def _strip_tags(string: str) -> str:
    """ Removes everything in the form '<...>'. """
    return re.sub(_TAG_PATTERN, "", string)


def _map(text_data: str) -> dict[str, str]:
    """ Parses the table from
        https://en.wikipedia.org/w/index.php?title=Template:List_of_hieroglyphs&action=edit """

    parsing_result = wtp.parse(text_data)
    data = []

    for t in parsing_result.templates:

        curr_data = {"gardiner": None, "description": None, "pron": None, "notes": None,
                     "unicode": None, "unicode_id": None, "meanings": []}
        gardiner_met = False

        for arg in t.arguments:
            if arg.name == "H":
                curr_data["unicode"] = arg.value.strip()
            elif arg.name.startswith("t"):
                curr_data["meanings"].append(arg.value.strip())
            elif arg.name == "desc":
                curr_data["description"] = arg.value.strip()
            elif arg.name == "gardiner":
                gardiner_met = True
                curr_data["gardiner"] = _strip_tags(arg.value).strip()
            elif arg.name == "unicode":
                curr_data["unicode_id"] = arg.value.strip()
            elif arg.name == "pron":
                curr_data["pron"] = arg.value.strip()
            elif arg.name == "notes":
                curr_data["notes"] = arg.value.strip()
            elif arg.name not in _IGNORED_ARGS:
                raise Exception(f"Unknown field: [{arg.name.strip()}] arg_value = {arg.value}")

        # rows without the information of interest are skipped
        if not gardiner_met or (curr_data["unicode"] is None and curr_data["unicode_id"] is None):
            logging.debug("This line does not contain any Gardiner code! %s",
                          str(t).replace("\n", " "))
        else:
            data.append(curr_data)

    # converting codes to the 8-character form, e.g. "00013000"
    return {row["gardiner"]: row["unicode_id"].zfill(8) for row in data}


class GardinerToUnicodeMap:
    """ A bidirectional mapping between Gardiner's Sign List codes
        (e.g. ``"A1"``) and Egyptian-Hieroglyphs-block Unicode code points
        (e.g. ``"00013000"`` / ``77824`` / ``"𓀀"``).

        All lookup tables are precomputed once at construction time; every
        ``to_*`` method is then an O(1) dictionary access. """

    def __init__(self, path: str = None):

        logging.debug("Parsing \"Template:List_of_hieroglyphs\"...")

        if path is None:
            from . import data
            raw_text = files(data).joinpath("wikipedia_table.wiki").read_text(encoding="utf-8").strip()
        else:
            with open(path, encoding="utf-8") as f:
                raw_text = f.read().strip()

        # Primary tables: Gardiner code <-> 8-char uppercase hex string
        self.gardiner2unicode: dict[str, str] = _map(raw_text)
        self.unicode2gardiner: dict[str, str] = {v: k for k, v in self.gardiner2unicode.items()}

        # checking that the mapping is a bijection
        assert len(self.gardiner2unicode) == len(self.unicode2gardiner)

        # Derived tables for O(1) lookups
        self._gardiner_to_int: dict[str, int] = {
            code: int(hx, 16) for code, hx in self.gardiner2unicode.items()
        }
        self._gardiner_to_char: dict[str, str] = {
            code: chr(value) for code, value in self._gardiner_to_int.items()
        }
        self._int_to_gardiner: dict[int, str] = {
            value: code for code, value in self._gardiner_to_int.items()
        }
        self._char_to_gardiner: dict[str, str] = {
            char: code for code, char in self._gardiner_to_char.items()
        }

        logging.debug("Table parsed successfully. Map of size [%d] was built.",
                      len(self.gardiner2unicode))

    def to_unicode_hex(self, code: str) -> Optional[str]:
        """ Gardiner code -> 8-digit hex string, e.g. ``"A1" -> "00013000"``. """
        return self.gardiner2unicode.get(code)

    def to_unicode_int(self, code: str) -> Optional[int]:
        """ Gardiner code -> Unicode code point as int, e.g. ``"A1" -> 77824``. """
        return self._gardiner_to_int.get(code)

    def to_unicode_char(self, code: str) -> Optional[str]:
        """ Gardiner code -> Unicode character, e.g. ``"A1" -> "𓀀"``. """
        return self._gardiner_to_char.get(code)

    def to_gardiner_from_hex(self, hex_code: str) -> Optional[str]:
        """ 8-digit hex string -> Gardiner code, e.g. ``"00013000" -> "A1"``.
            Input is case-insensitive. """
        return self.unicode2gardiner.get(hex_code.upper())

    def to_gardiner_from_int(self, unicode_decimal_number: int) -> Optional[str]:
        """ Unicode code point as int -> Gardiner code, e.g. ``77824 -> "A1"``. """
        return self._int_to_gardiner.get(unicode_decimal_number)

    def to_gardiner_from_chr(self, char: str) -> Optional[str]:
        """ Single Unicode character -> Gardiner code, e.g. ``"𓀀" -> "A1"``. """
        assert len(char) == 1
        return self._char_to_gardiner.get(char)
