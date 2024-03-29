from operator import itemgetter

from src.data import DFCLASS_ORDER, getdfclass, getselfskills_context, skills_by_dfclass
from src.util import write_json

def build_dfclass():
  
  dfclasses = [*map(getdfclass, DFCLASS_ORDER)]
  
  for dfclass in dfclasses:
    # skills = getskills_context(dfclass["name"])
    skills = skills_by_dfclass(dfclass["name"])
    skills.sort(key=itemgetter("name"))
    skills.sort(key=itemgetter("level"))
    selfskills = getselfskills_context(dfclass["name"])
    selfskills.sort(key=itemgetter("name"))
    dfclass["skills"] = [*map(itemgetter("id"), skills)]
    dfclass["selfSkills"] = [*map(itemgetter("id"), selfskills)]
    
  write_json(dfclasses, "./dist/data/dfclass.json")


if __name__ == "__main__":
  build_dfclass()
