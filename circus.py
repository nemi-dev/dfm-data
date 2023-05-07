import csv, json
from typing import Literal
from os import makedirs
from os.path import join

from src.data import baseitem_60Epic, getdfclass
from src.id import genid
from util import write_json
"""
환(幻) 아이템 특징

- "세비지 스로우"는 스킬 올라가는게 다르다
  (무기/상의/하의=G-35L 섬광류탄)
  (머리어깨/벨트/신발=G-61 중력류탄)
  (팔찌/목걸이/반지/보조장비=G-18C 빙결류탄)

- 모든 [무기]는 [{스킬A} 공격력 10% 증가, 스킬 공격력 30% 증가]가 붙어있다.
- 모든 [상의/하의]는 [{스킬B} 공격력 7% 증가, 힘/지능 3% 증가]가 붙어있다.
- 모든 [머리어깨/벨트/신발]은 [{스킬A} 공격력 5% 증가, 물리/마법 크리티컬 +35]가 붙어있다.
- 모든 [팔찌/목걸이/반지]는 [{스킬B} 공격력 5% 증가, 모든 속성 강화 +5]가 붙어있다.
- 모든 [보조장비]는 [{스킬A} 공격력 5% 증가, 물리/마법 공격력 +39]가 붙어있다.

"""


# 상의/하의
co = {
  "str_inc": 3,
  "int_inc": 3,
}

# 머리어깨/벨트/신발
neck = {
  "crit_ph": 35,
  "crit_mg": 35
}

# 팔찌/목걸이/반지
acce = {
  "el_fire": 5,
  "el_ice":  5,
  "el_lght": 5,
  "el_dark": 5
}

# 보조장비
supo = {
  "atk_ph": 39,
  "atk_mg": 39
}

ARMORATTRS = {
  "상의"   : co,
  "하의"   : co,
  "머리어깨": neck,
  "벨트"   : neck,
  "신발"   : neck
}

def skill(sk_name: str, val: int) -> dict[Literal["sk_val"], dict[str, int]]:
  '''특정 스킬의 모든 계수를 증가시키는 효과를 만든다.'''
  return {
    "sk_val": {
      sk_name: val
    }
  }

class Circus:
  def __init__(self, dfclassname: str, isetname: str, skillnameA: str, skillnameB: str) -> None:
    self.isetname = isetname
    self.dfclassname = dfclassname
    self.skillnameA = skillnameA
    self.skillnameB = skillnameB
  
  def __repr__(self) -> str:
    return f"{self.isetname} ({self.dfclassname})"
  
  @property
  def dfclass(self):
    return getdfclass(self.dfclassname)
  
  @property
  def majorweapon(self):
    return self.dfclass["weapons"][0]
  
  def createbase(self, name: str, itype: str):
    id = genid(name)
    return {
      "id": id,
      "name": name,
      "level": 60,
      "rarity": "Epic",
      "itype": itype,
      "setOf": [ f"환(幻): {self.isetname}" ],
      "who": [ self.dfclassname ],
      "content": [ "환영극단 2막" ]
    }
  
  def armor(self, armorpart: Literal["상의", "하의", "머리어꺠", "벨트", "신발"]):
    suffix = "어깨" if armorpart == "머리어깨" else armorpart
    name = f"환(幻): {self.isetname} - {suffix}"
    material = self.dfclass["armorMaterial"]
    sk_name, sk_val = (self.skillnameA, 5) if armorpart in ["머리어깨", "벨트", "신발"] else (self.skillnameB, 7)
    
    item = {
      **self.createbase(name, armorpart),
      "image": f"환영극단 {material} {armorpart}",
      "material": material,
      "attrs": {
        **ARMORATTRS[armorpart],
        **skill(sk_name, sk_val)
      }
    }
    
    return item
  
  def accessory(self, itype: Literal["팔찌", "목걸이", "반지"]):
    name = f"환(幻): {self.isetname} - {itype}"
    sk_name = self.skillnameB
    
    item = {
      **self.createbase(name, itype),
      "image": f"환영극단 {itype}",
      "attrs": {
        **baseitem_60Epic(itype)["attrs"],
        **skill(sk_name, 5),
        **acce
      }
    }
    return item
  
  def support(self):
    name = f"환(幻): {self.isetname} - 보조장비"
    item = {
      **self.createbase(name, "보조장비"),
      "image": "환영극단 보조장비",
      "attrs": {
        **baseitem_60Epic("보조장비")["attrs"],
        **supo
      }
    }
    return item
  
  def weapon_one(self):
    itype = self.majorweapon
    name = f"환(幻): {self.isetname} - {itype}"
    item = {
      **self.createbase(name, itype),
      "image": f"환영극단 {itype}",
      "attrs": {
        "sk_inc": 30,
        **skill(self.skillnameA, 10),
        **baseitem_60Epic(itype)["attrs"]
      }
    }
    return item
  
  

with open("illusion-first.tsv", encoding="UTF-8", newline='') as r:
  reader = csv.DictReader(r, delimiter='\t')
  clist = [*reader]
  
for row in clist:
  cir = Circus(**row)
  dirname = f"./data/item/환2/{cir.dfclassname}"
  makedirs(dirname, exist_ok=True)
  for armorpart in ["상의", "하의", "머리어깨", "벨트", "신발"]:
    suffix = "어깨" if armorpart == "머리어깨" else armorpart
    item = cir.armor(armorpart)
    basename = f"환-{cir.isetname} - {suffix}.json"
    jsonpath = join(dirname, basename)
    write_json(item, jsonpath)

  for accepart in ["팔찌", "목걸이", "반지"]:
    item = cir.accessory(accepart)
    basename = f"환-{cir.isetname} - {accepart}.json"
    jsonpath = join(dirname, basename)
    write_json(item, jsonpath)
  
  item = cir.weapon_one()
  basename = f"환-{cir.isetname} - {cir.majorweapon}.json"
  jsonpath = join(dirname, basename)
  write_json(item, jsonpath)

  
  item = cir.support()
  basename = f"환-{cir.isetname} - 보조장비.json"
  jsonpath = join(dirname, basename)
  write_json(item, jsonpath)

  
