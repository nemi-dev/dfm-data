import json
from os import makedirs
from shutil import rmtree

from utils.shake import shake

shake("./data")
shake("./img")

from utils.data import isets_array, items_array, read_json
from utils.pickimage import pick_image
from utils.id import genid

rmtree("./dist", ignore_errors=True)
makedirs("./dist/data", exist_ok=True)
makedirs("./dist/public/img/item", exist_ok=True)


base_attrs_schema = read_json("./schema/base-attrs.json")
keys = [*base_attrs_schema["properties"].keys()]

def test_attr(item: dict):
  mixin_keys = []
  for key in keys:
    if key in item:
      mixin_keys.append(key)
      
  if len(mixin_keys) > 0:
    print(f'{item.get("name")}에 옵션 {", ".join(mixin_keys)}이(가) 믹스인으로 들어 있어요!')

for item in items_array:
  item["id"] = genid(item["name"])
  pick_image(item)
  test_attr(item)

with open("./dist/data/items.json", "w", encoding="utf-8") as write:
  json.dump(items_array, write, indent=None, separators=(",", ":"), ensure_ascii=False)

with open("./dist/data/itemsets.json", "w", encoding="utf-8") as write:
  json.dump(isets_array, write, indent=None, separators=(",", ":"), ensure_ascii=False)

