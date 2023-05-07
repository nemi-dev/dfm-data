import json
from os import makedirs

from src.data import dfitems, dfisets
from src.pickimage import pick_image
from src.util import write_json
from operator import attrgetter

def build_items():

  makedirs("./dist/data", exist_ok=True)
  makedirs("./dist/public/img/item", exist_ok=True)

  for item in dfitems():
    pick_image(item)

  write_json([*map(attrgetter("json"), dfitems())], "./dist/data/items.json")
  write_json([*map(attrgetter("json"), dfisets())], "./dist/data/itemsets.json")

