from functools import cache
from operator import itemgetter

from .data import DFIset, DFItem

RARITY = ["Epic", "Unique", "Rare", "Uncommon", "Common"]
def rarity(item):
  r = item.json.get("rarity", "Common")
  return RARITY.index(r)

@cache
def priority_iset():
  with open("./priority-iset.txt", encoding="UTF-8") as r:
    return [s for line in r if (s := line.strip())]
  
@cache
def priority_item():
  with open("./priority-item.txt", encoding="UTF-8") as r:
    return [s for line in r if (s := line.strip())]

last_priority = len(priority_iset()) + len(priority_item())


def key_priority(item: DFItem):
  iset: list[str] = item.get("setOf", [None])
  if iset == "all": return -1
  
  iset_pick = iset[0]
  if iset_pick in priority_iset():
    return priority_iset().index(iset_pick)
  
  if item["name"] in priority_item():
    return len(priority_iset()) + priority_item().index(item["name"])
  
  return last_priority


def key_priority_isetonly(iset: DFIset):
  if iset["name"] in priority_iset():
    return priority_iset().index(iset["name"])
  
  return last_priority
  
def sort_items(items: list):
  items.sort(key=itemgetter("name"))
  items.sort(key=key_priority)
  items.sort(key=rarity)
  items.sort(key=lambda x: x.get("level", 1), reverse=True)

def sort_isets(isets: list):
  isets.sort(key=key_priority_isetonly)
