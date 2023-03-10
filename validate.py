from jschon import create_catalog, JSON, JSONSchema
from utils.data import items_array, isets_array
from utils.read_json import read_json

create_catalog('2020-12')

item_schema = JSONSchema(read_json("./item.json"))
iset_schema = JSONSchema(read_json("./iset.json"))

for item in items_array:
  result = item_schema.evaluate(item)
  result.output("basic")

