
def skval(lvA: float, valA: float, lvB: float, valB: float):
  """특정 스킬에 들어간 공격에 대해, 두 지점에서의 계수 차이를 이용해 base와 inc 값을 얻는다."""
  inc = (valB - valA) / (lvB - lvA)
  baseA = valA - (inc * lvA)
  baseB = valB - (inc * lvB)
  return baseA, baseB, inc


if __name__ == "__main__":
  from sys import argv

  lvA, lvB, valA, valB = map(float, argv[1:])
  baseA, baseB, inc = skval(lvA, valA, lvB, valB)
  print(f"""\
  baseA= {baseA}
  baseB= {baseB}
  inc=   {inc}
  """)
