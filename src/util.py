import json, re
from os import makedirs, renames, walk
from os.path import dirname, join
from unicodedata import normalize


def compound(a: float, b: float):
  """(1 + a/100)*(1 + b/100) - 1 을 구한다."""
  return a + b + a * b / 100

def sanitize_filename(s: str):
  """s를 basename으로 취급하여 윈도우에서 사용가능한 파일 이름으로 바꾼다."""
  return re.sub(r"[\<\>\:\"\'\?\*\\\/\|]", "-", s)

def shake(p):
  """
  macOS에서 NFD로 일반화된 한글 파일 이름을 NFC로 바꾼다.
  """
  target = []
  targetd = []
  for dirname, dirs, files in walk(p):
    for fname in files:
      target.append(join(dirname, fname))
    for dname in dirs:
      targetd.append(join(dirname, dname))
  for t in target:
    u = normalize("NFC", t)
    if t != u:
      renames(t, u)
  for t in targetd:
    u = normalize("NFC", t)
    if t != u:
      renames(t, u)

def read_json(fname: str) -> dict:
  with open(fname, encoding="utf-8") as read:
    return json.load(read)

def write_json(obj, fname: str, pretty=False):
  options = { "indent": 2, "separators": (',', ': ') } if pretty else { "indent": None, "separators": (',', ':')}
  makedirs(dirname(fname), exist_ok=True)
  with open(fname, "w", encoding="UTF-8") as out:
    json.dump(obj, out, ensure_ascii=False, **options)

def skval(lvA: float, valA: float, lvB: float, valB: float):
  """특정 스킬에 들어간 공격에 대해, 두 지점에서의 계수 차이를 이용해 base와 inc 값을 얻는다."""
  inc = (valB - valA) / (lvB - lvA)
  baseA = valA - (inc * lvA)
  baseB = valB - (inc * lvB)
  return baseA, baseB, inc
