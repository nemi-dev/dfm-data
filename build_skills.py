from src.data import getselfskill, search_skill, DFCLASS_ORDER, skills_by_dfclass
from src.util import read_json, write_json, skval

from typing import TypedDict, NotRequired, Union, List, Dict

from os.path import basename
from glob import glob
from math import ceil

def is_secant(skVal):
  """
  `skVal`이 [Number, Number] 타입인지 확인한다.
  """
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




Number = Union[int, float]

class AtProps(TypedDict):
  maxHit: NotRequired[int]
  chargeup: NotRequired[Number]

class SKInputType(TypedDict):
  # maxHits: NotRequired[Dict[str, int]]
  atProps: NotRequired[AtProps]
  values: List[Dict[str, Number]]

class AttackType(TypedDict):
  atName: str
  value: TypedDict('Poly', { 'base': Number, 'inc': Number })
  maxHit: NotRequired[Number]

def convert_input_to_polynomial(input: SKInputType):
  value1, value2 = input["values"]
  atProp = input.get("atProps", {})
  lv1, lv2 = value1.pop("at"), value2.pop("at")
  atnames = [*value1.keys()]
  attacks: List[AttackType] = list()
  for atname in atnames:
    val1, val2 = value1[atname], value2[atname]
    base1, base2, inc = skval(lv1, val1, lv2, val2)
    attack: AttackType = {
      "atName": atname,
      "value": {
        "base": ceil((base1 + base2) / 2 * 10000) / 10000,
        "inc": ceil(inc * 10000) / 10000
      },
      **atProp
    }
    attacks.append(attack)
  
  return attacks

  

def polyfy_writeback(json_name):
  askill = read_json(json_name)
  modified = polyfy(askill)
  if modified:
    write_json(askill, json_name, True)


def apply_input_into(dinput: dict):
  """
  { "vaName": "name", "input": ? } 형식을
  { "vaName": "name", "attacks": ? } 형식으로 바꾼다.
  """
  # input = vinput.pop("input")
  if "input" in dinput:
    input = dinput["input"]
    attacks = convert_input_to_polynomial(input)
    dinput["attacks"] = attacks
  
  if "vinput" in dinput:
    vinput_ = dinput["vinput"]
    variants = [{ "vaName": i["vaName"], "attacks": convert_input_to_polynomial(i) } for i in vinput_]
    dinput["variants"] = variants
    
  return dinput


def convert_poly(json_name: str):
  askill = read_json(json_name)
  out_name = json_name.replace('/ainput/', '/skill/')
  if input := askill.get("input", None):
    # askill.pop("input")
    askill["attacks"] = convert_input_to_polynomial(input)
  if vinput := askill.get("vinput", None):
    # askill.pop("vinput")
    askill["variant"] = map(apply_input_into, vinput)
  write_json(askill, out_name, True)


def build_skills():
  
  # for askill_name in glob("./data/skill/**/*.json", recursive=True):
  #   polyfy_writeback(askill_name)
    
  for askill_name in glob("./data/ainput/**/*.json", recursive=True):
    convert_poly(askill_name)
  
  skills: list[dict] = []
  for dfcname in DFCLASS_ORDER:
    skills_dfc = skills_by_dfclass(dfcname)
    skills.extend(skills_dfc)
    
  write_json(skills, "./dist/data/skills.json")
  
  selfskills = getselfskill("")
  write_json(selfskills, "./dist/data/selfskills.json")

if __name__ == "__main__":
  build_skills()
  