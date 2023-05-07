import csv
from typing import Literal
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

supo = {
  "atk_ph": 39,
  "atk_mg": 39
}

def skill(sk_name: str, val: int) -> dict[Literal["sk_val"], dict[str, int]]:
  '''특정 스킬의 모든 계수를 증가시키는 효과를 만든다.'''
  return {
    "sk_val": {
      sk_name: val
    }
  }

class Illusion:
  def __init__(self, dfclassname: str, isetname: str, skillnameA: str, skillnameB: str) -> None:
    self.isetname = isetname
    self.dfclassname = dfclassname
    self.skillnameA = skillnameA
    self.skillnameB = skillnameB
  
  def __repr__(self) -> str:
    return f"{self.isetname} ({self.dfclassname})"
  
  

with open("illusion.tsv", encoding="UTF-8", newline='') as r:
  reader = csv.DictReader(r, delimiter='\t')
  for row in reader:
    i = Illusion(**row)
    print(i)
