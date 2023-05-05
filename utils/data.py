from functools import cache
from glob import glob

from utils.id import genid
from .read_json import read_json
import json

RARITY = ["Epic", "Unique", "Rare", "Uncommon", "Common"]
def rarity(item):
  r = item.json.get("rarity", "Common")
  return RARITY.index(r)

DFITEM_KEYS_ORDER = ["id", "name", "level", "rarity", "itype", "image", "overlay", "setOf", "who", "content", "part", "material", "ArtiColor", "attrs", "branch", "gives", "exclusive", "misc"]


class JSONDictLike:
  
  def __getitem__(self, key): return self.json[key]
  def __setitem__(self, key, value): self.json[key] = value
  def __contains__(self, key): return key in self.json
  
  def __iter__(self): return iter(self.json)
  
  def get(self, key, default = None): return self.json.get(key, default)
  def items(self): return self.json.items()
  
  @property
  def fname(self):
    return self._fname
    
  def write_back(self):
    with open(self._fname, "w", encoding="UTF-8") as w:
      json.dump(self.json, w, ensure_ascii=False, separators=(', ', ': '), indent=2)


class DFItem(JSONDictLike):

  def __init__(self, fname: str) -> None:
    super().__init__()
    self._fname = fname
    _d = read_json(fname)
    if not "id" in _d: _d["id"] = genid(_d["name"])
    self.json = { key: _d.pop(key) for key in DFITEM_KEYS_ORDER if key in _d }
    self.json.update(_d)
  


@cache
def dfitems():
  fnames = glob("data/item/**/*.json", recursive=True)
  ilist = sorted(map(DFItem, fnames), key=lambda x: x.json["name"])
  ilist.sort(key=rarity)
  ilist.sort(key=lambda x: x.json.get("level", 1), reverse=True)
  return ilist

class DFIset(JSONDictLike):
  def __init__(self, fname: str) -> None:
    super().__init__()
    self._fname = fname
    _d = read_json(fname)
    if not "id" in _d:
      _d["id"] = genid(_d["name"])
    self.json = { "id": _d.pop("id"), "name": _d.pop("name") }
    self.json.update(_d)

@cache
def dfisets():
  fnames = glob("data/itemset/**/*.json", recursive=True)
  return sorted(map(DFIset, fnames), key=lambda x: x.json["name"])
  

