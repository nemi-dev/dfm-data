"""
"특정 스킬 공격력 증가"를 테스트한다.
"""

from sys import argv

from functools import reduce

from src.data import search_skill
from src.util import compound


if __name__ == "__main__":
  sk_name, sk_lv_str, *sk_inc_str = argv[1:]
  sk_lv = int(sk_lv_str)
  sk_inc = [*map(float, sk_inc_str)]


  sk_inc_reduced = reduce(compound, sk_inc, 0.)
  sk_inc_ft = 1 + sk_inc_reduced / 100

  print(f"skinc = {sk_inc_reduced}%")
  print(f"skinc_factor = {sk_inc_ft}")
  
  sks = search_skill(sk_name)

  for sk in sks:
    attacks: list[dict] = sk["attacks"]
    for attack in attacks:
      if type(attack["value"]) in [int, float]:
        val_real = float(attack["value"])
      else:
        val_real = attack["value"]["base"] + attack["value"]["inc"] * sk_lv
      print(f"{sk['name']}[{attack['atName']}](Lv.{sk_lv}) {val_real * sk_inc_ft}%")
