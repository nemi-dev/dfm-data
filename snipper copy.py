import json
import os
import re
from os.path import splitext


def read_json(fname: str):
  with open(fname, encoding="utf-8") as read:
    return json.load(read)

# bases = read_json("./armorbase.json")
bases = os.listdir("./data/baseitem")
snippet_list = {}

for item_fname in bases:
  item = read_json("./data/baseitem/" + item_fname)
  item_name = splitext(item_fname)[0]
  item["name"] = r"${0:$TM_FILENAME_BASE}"
  spec = {}
  body = json.dumps(item, indent=2, separators=(", ", ": "), ensure_ascii=False).split("\n")
  spec["scope"] = "json"
  spec["body"] = [*body]
  snippet_list[item_name] = spec
  
with open("60epic-weapons.code-snippets", "w", encoding="utf-8") as w:
  json.dump(snippet_list, w, indent=2, separators=(", ", ": "), ensure_ascii=False)
