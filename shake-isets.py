from typing import Dict
from utils.data import read_json
from glob import glob

import json

base_attrs_schema = read_json("./schema/base-attrs.json")
keys: list[str] = [*base_attrs_schema["properties"].keys()]

iset_files: list[str] = glob("data/itemset/**/*.json", recursive=True)

def shake(isetpath: str):
  iset: Dict[str, Dict] = read_json(isetpath)
  for setcount, setprops in iset.items():
    if setcount.isnumeric():
      print(f'{iset["name"]}[{setcount}]')
      setprops["name"] = f'{iset["name"]}[{setcount}]'
      # base_attrs = {}
      # for key in keys:
      #   if key in setprops:
      #     base_attrs[key] = setprops.pop(key)
      
      # if len(base_attrs) > 0:
      #   setprops["attrs"] = base_attrs
  with open(isetpath, "w", encoding="utf-8") as w:
    json.dump(iset, w, ensure_ascii=False, indent=2)
      
        
for i in iset_files: shake(i)
