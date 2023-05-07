from glob import glob
from .read_json import read_json

def getskill(sk_name: str):
  sk_filename = glob(f"./data/skill/**/{sk_name}.json")[0]
  return read_json(sk_filename)
