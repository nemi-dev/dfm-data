from functools import cache
from glob import glob

from .id import genid
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
  fnames = glob("./data/item/**/*.json", recursive=True)
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
  fnames = glob("./data/itemset/**/*.json", recursive=True)
  return sorted(map(DFIset, fnames), key=lambda x: x.json["name"])
  
@cache
def getskill(sk_name: str):
  sk_found = glob(f"./data/skill/**/{sk_name}.json")
  if not sk_found: raise FileNotFoundError(f"스킬이 없어요!!: {sk_name}")
  if len(sk_found) > 1: raise Exception(f"같은 이름의 스킬이 2개 이상 있어요!!: {sk_found}")
  sk_filename = sk_found[0]
  
  return read_json(sk_filename)

DFCLASS_ORDER = [
  "버서커", "소울브링어", "웨펀마스터", "아수라",
  "레인저(남)", "런처(남)", "메카닉", "스핏파이어",
  "넨마스터", "스트라이커", 
  "엘레멘탈마스터", "마도학자", 
  "크루세이더(여)", "미스트리스", "이단심판관", "무녀",
  "소드마스터", "베가본드", "데몬슬레이어", "다크템플러",
  "크루세이더(남)", "인파이터", 
  "와일드베인", "윈드시어",
  "레인저(여)", "런처(여)"
]

def getdfclass(dfclassname: str):
  return read_json(f"./data/dfclass/{dfclassname}.json")
