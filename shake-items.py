from typing import Dict
from utils.data import read_json
from glob import glob

import json

base_attrs_schema = read_json("./schema/base-attrs.json")
attrKeys: list[str] = [*base_attrs_schema["properties"].keys()]

items: list[str] = glob("data/item/**/*.json", recursive=True)

def shake(jsonpath: str):
  item: Dict[str, Dict] = read_json(jsonpath)
  
  # with open(jsonpath, "w", encoding="utf-8") as w:
  #   json.dump(item, w, ensure_ascii=False, indent=2)
      
        
for i in items: shake(i)
