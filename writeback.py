from sys import stderr
from src.data import dfisets, dfitems

from src.id import genid

def assign_id(item: dict):
  name = item.get("name", None)
  if name == None:
    print("The item has no name!", file=stderr)
    return
  
  id = genid(name)
  return {
    "id": id,
    **item
  }

if __name__ == "__main__":
  for i in dfitems():
    i.write_back()
  
  for i in dfisets():
    i.write_back()
    