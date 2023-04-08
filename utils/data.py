from glob import glob
from operator import itemgetter
from .read_json import read_json

RARITY = ["Epic", "Unique", "Rare", "Uncommon", "Common"]
def rarity(item: dict):
  r = item.get("rarity", "Common")
  return RARITY.index(r)


item_files: list[str] = glob("data/item/**/*.json", recursive=True)
iset_files: list[str] = glob("data/itemset/**/*.json", recursive=True)


# 레벨 -> 레어도 -> 이름 순으로 정렬하려면
# Python에서는 이름 -> 레어도 -> 레벨 순으로 sort()를 사용한다.
# (Python sort()의 stability : 정렬 키가 같은 값들끼리는 정렬 전에 나타난 순서가 유지된다.)

items_array = sorted(map(read_json, item_files), key=itemgetter("name"))
items_array.sort(key=rarity)
items_array.sort(key=lambda x: x.get("level", 1), reverse=True)

isets_array = sorted(map(read_json, iset_files), key=itemgetter("name"))
