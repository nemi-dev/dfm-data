from src.data import getselfskill, search_skill, DFCLASS_ORDER, skills_by_dfclass
from src.util import read_json, write_json, skval

from glob import glob
from math import ceil

def is_secant(skVal):
  if not type(skVal) == list or len(skVal) != 2: return False
  A, B = skVal
  _types = (int, float)
  return type(A) in _types and type(B) in _types

def polyfy(askill: dict):
  s_level = askill.pop("s_level", None)
  s_atNames = askill.pop("s_atNames", None)
  s_values_1 = askill.pop("s_values_1", None)
  s_values_2 = askill.pop("s_values_2", None)
  
  test = (s_level, s_atNames, s_values_1, s_values_2)
  if not any(test):
    return False
  
  if not all(test):
    s = f"공격스킬 \"{askill['name']}\" 에 어떤 입력값이 없어요! "
    e = ValueError(s)
    raise e
  
  attacks: list[dict] = []
  lv1, lv2 = s_level
  
  for atName, val1, val2 in zip(s_atNames, s_values_1, s_values_2, strict=True):
    base1, base2, inc = skval(lv1, val1, lv2, val2)
    attack = {
      "atName": atName,
      "value": {
        "base": ceil((base1 + base2) / 2 * 10000) / 10000,
        "inc": ceil(inc * 10000) / 10000
      }
    }
    attacks.append(attack)
  
  askill["attacks"] = attacks
  
  return True
      

def polyfy_writeback(json_name):
  askill = read_json(json_name)
  modified = polyfy(askill)
  if modified:
    write_json(askill, json_name, True)


def build_skills():
  
  for askill_name in glob("./data/skill/**/*.json", recursive=True):
    polyfy_writeback(askill_name)
  
  skills: list[dict] = []
  for dfcname in DFCLASS_ORDER:
    skills_dfc = skills_by_dfclass(dfcname)
    skills.extend(skills_dfc)
    # skills += skills_dfc
    
  # skills = search_skill("")
  write_json(skills, "./dist/data/skills.json")
  
  selfskills = getselfskill("")
  write_json(selfskills, "./dist/data/selfskills.json")

if __name__ == "__main__":
  build_skills()
  