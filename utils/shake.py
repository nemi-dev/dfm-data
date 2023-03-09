from os import renames, walk
from os.path import join
from unicodedata import normalize



def shake(p):
  """
  똥쿡의 가호를 받은 자는 이 시련을 거쳐야 할지니.
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