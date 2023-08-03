import json
import yaml
from glob import glob
from os import makedirs
from os.path import dirname, splitext

jsons = glob("./data/**/*.json", recursive=True)

for fname in jsons:
  with open(fname, encoding="utf-8") as read:
    d = json.load(read)
    
  yml_dest = splitext(fname.replace("./data/", "./yaml/"))[0] + '.yaml'
  
  makedirs(dirname(yml_dest), exist_ok=True)
  
  with open(yml_dest, "w", encoding="utf-8") as write:
    yaml.dump(d, write, allow_unicode=True, sort_keys=False)

