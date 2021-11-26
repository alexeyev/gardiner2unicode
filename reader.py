# coding: utf-8

import wikitextparser as wtp


def map(path_templates_list: str = "wikipedia_table.wiki"):

    parsing_result = wtp.parse(open(path_templates_list, "r+", encoding="utf-8").read().strip())
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
                raise Exception(f"Who are you, Mr. {arg.name.strip()}? arg_value = {arg.value}")

        if not gardiner_met or (curr_data.get("unicode", None) is None and curr_data["unicode_id"] is None):
            t = str(t).replace('\n', ' ')
            print(f"This line does not contain any Gardiner code! {t}")
        else:
            data.append(curr_data)

    result = {}

    for dictionary in data:
        result[dictionary["gardiner"]] = (dictionary["unicode_id"], dictionary["unicode"])

    return result

if __name__ == "__main__":
    print(map())
