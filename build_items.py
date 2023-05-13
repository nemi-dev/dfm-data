from os import makedirs
from operator import attrgetter

from src.data import dfitems, dfisets
from src.ordering import sort_isets, sort_items
from src.pickimage import pick_image
from src.util import write_json

def build_items():

  makedirs("./dist/data", exist_ok=True)
  makedirs("./dist/public/img/item", exist_ok=True)

  items = dfitems()
  isets = dfisets()
  
  sort_items(items)
  sort_isets(isets)
  
  for item in items: pick_image(item)
  
  write_json([*map(attrgetter("json"), items)], "./dist/data/items.json")
  write_json([*map(attrgetter("json"), isets)], "./dist/data/itemsets.json")

if __name__ == "__main__":
  build_items()
