# coding: utf-8

import logging
from functools import lru_cache
from typing import Optional, Dict

import wikitextparser as wtp


def _map(text_data: str) -> Dict[str, str]:
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
                curr_data["gardiner"] = arg.value.strip()
            elif arg.name == "unicode":
                curr_data["unicode_id"] = arg.value.strip()
            elif arg.name == "pron":
                curr_data["pron"] = arg.value.strip()
            elif arg.name == "notes":
                curr_data["notes"] = arg.value.strip()
            elif arg.name != "1" and not arg.name == "2" \
                    and not arg.name == "date" \
                    and not arg.name == "qid" \
                    and not arg.name == "reason" \
                    and not arg.name == "url" and not arg.name == "website" and not arg.name == "title":
                raise Exception(f"Unknown field: [{arg.name.strip()}] arg_value = {arg.value}")

        if not gardiner_met or (curr_data.get("unicode", None) is None and curr_data["unicode_id"] is None):
            t = str(t).replace('\n', ' ')
            logging.debug(f"This line does not contain any Gardiner code! {t}")
        else:
            data.append(curr_data)

    result = {}

    for dictionary in data:
        eight_letter_unicode = dictionary['unicode_id'].zfill(8)
        result[dictionary["gardiner"]] = eight_letter_unicode  # , dictionary["unicode"])

    return result


class GardinerToUnicodeMap(object):

    def __init__(self, path: str = None):

        logging.debug("Reading archive...")

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

    @lru_cache(maxsize=10000)
    def to_unicode_hex(self, code: str) -> Optional[str]:
        return self.gardiner2unicode.get(code, None)

    @lru_cache(maxsize=10000)
    def to_unicode_int(self, code: str):
        hx = self.to_unicode_hex(code)
        return int(hx, 16) if hx is not None else None
