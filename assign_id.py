from glob import glob
from sys import argv

from src.id import genid
from src.util import read_json, write_json

def do_writeback(context: str):
  g = glob(f"./data/{context}/**/*.json", recursive=True)
  for json_name in g:
    j = read_json(json_name)
    if "id" in j: continue
    if not "name" in j: continue
    
    j2 = { "id": genid(j["name"]), **j }
    write_json(j2, json_name, pretty=True)
    
if __name__ == "__main__":
  do_writeback(argv[1])
