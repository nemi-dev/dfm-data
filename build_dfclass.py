from operator import itemgetter

from src.data import DFCLASS_ORDER, getdfclass, getskills_context
from src.util import write_json

def build_dfclass():
  
  dfclasses = [*map(getdfclass, DFCLASS_ORDER)]
  
  for dfclass in dfclasses:
    skills = getskills_context(dfclass["name"])
    selfskills = getskills_context(dfclass["name"])
    dfclass["skills"] = [*map(itemgetter("name"), skills)]
    dfclass["selfSkills"] = [*map(itemgetter("name"), selfskills)]
    
  write_json(dfclasses, "./dist/data/dfclass.json")


if __name__ == "__main__":
  build_dfclass()
