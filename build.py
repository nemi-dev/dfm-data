from os import makedirs, walk, rename
from os.path import basename, splitext, join
from sys import stderr
from unicodedata import normalize

from shutil import copy2
import glob, json, re


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
      rename(t, u)
  for t in targetd:
    u = normalize("NFC", t)
    if t != u:
      rename(t, u)

def sanitize_filename(s: str):
  return re.sub(r"[\<\>\:\"\'\?\*\\\/\|]", "-", s)

def read_json(fname: str):
  with open(fname, encoding="utf-8") as read:
    return json.load(read)

def test_name(item: dict, fname: str):
  real_filename_noext = splitext(basename(fname))[0]
  if sanitize_filename(item["name"]) != real_filename_noext:
    print(f"파일 이름({real_filename_noext})이 아이템 이름({item['name']})이랑 달라요!", file=stderr)

def test_image(item: dict, fname: str):
  # 방어구재질에 "itype"이 없다
  if item["name"].startswith("<"): return
  image_key_to_find = item.get("image", sanitize_filename(item["name"]))
  if not (image_key_to_find in image_hash):
    print(f"아이템({item['name']})에 적절한 그림이 없어요!", file=stderr)


shake("./data")
shake("./img")


item_files: list[str] = glob.glob("data/item/**/*.json", recursive=True)
image_files: list[str] = glob.glob("img/item/**/*.png", recursive=True)

image_hash = {}

for image_fname in image_files:
  image_key = splitext(basename(image_fname))[0]
  if image_key in image_hash:
    print(f"아이템 아이콘이 겹쳐요!: [{image_fname}] vs [{image_hash[image_key]}]")
  image_hash[image_key] = image_fname


big_array = []

for item_fname in item_files:
  item: dict = read_json(item_fname)
  test_name(item, item_fname)
  test_image(item, item_fname)
  
  big_array.append(item)

makedirs("./dist/data", exist_ok=True)
makedirs("./dist/public/img/item", exist_ok=True)

for i in image_files:
  copy2(i, join("./dist/public/img/item", basename(i)))

with open("./dist/data/items.json", "w", encoding="utf-8") as write:
  json.dump(big_array, write, indent=None, separators=(",", ":"), ensure_ascii=False)

