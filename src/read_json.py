import json

def read_json(fname: str) -> dict:
  with open(fname, encoding="utf-8") as read:
    return json.load(read)
