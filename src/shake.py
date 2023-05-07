from os import renames, walk
from os.path import join
from unicodedata import normalize

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