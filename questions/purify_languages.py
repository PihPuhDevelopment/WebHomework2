import json

with open("languages.json", "r") as inp:
    in_dict = json.load(inp)

out_dict = {"languages": []}
for language in in_dict["itemListElement"]:
    out_dict["languages"].append(language["item"]["name"])

with open("langs.json", "w") as out:
    json.dump(out_dict, out)