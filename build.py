from os import makedirs, walk, rename
from os.path import basename, splitext, join, exists
from sys import stderr
from unicodedata import normalize

from shutil import copy2, rmtree
from hashlib import sha224
from base64 import b64encode
import glob, json, re

import quant

digest_table: dict[int, str] = {}
case_sensitive_table: dict[str, str] = {}

def indexy(i):
  try:
    return items_order.index(i["name"])
  except ValueError:
    return -1

def iindexy(i):
  try:
    return itemsets_order.index(i["name"])
  except ValueError:
    return -1
  
def fold(digest: bytes, original: str) -> bytes :
  chunk_size = len(digest) // 4
  digest_int = 0
  for i in range(0, 4):
    digest_int ^= int.from_bytes(digest[i * chunk_size:(i+1) * chunk_size])
  while digest_int in digest_table:
    if digest_table[digest_int] == original: break
    digest_int += 1
  digest_table[digest_int] = original
  return b64encode(digest_int.to_bytes(chunk_size), b"-_").strip(b'=')


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

def pick_image(item: dict, fname: str):
  name: str = item["name"]
  image_key_to_find = item.get("image", sanitize_filename(name))
  if not (image_key_to_find in image_hash):
    return print(f"아이템({item['name']})에 적절한 그림이 없어요!", file=stderr)
  image_digest = sha224(image_key_to_find.encode()).digest()
  image_dst = fold(image_digest, image_key_to_find).decode()
  item["image"] = image_dst
  if image_dst.lower() in case_sensitive_table:
    if case_sensitive_table[image_dst.lower()] != image_key_to_find:
      print("이미지 파일 해시가 겹쳐요!!", file=stderr)
  case_sensitive_table[image_dst.lower()] = image_key_to_find
  
  image_path = image_hash[image_key_to_find]
  image_dst_path = join("./dist/public/img/item", image_dst + ".png")
  if not exists(image_dst_path):
    # copy2(image_path, image_dst_path)
    quant.quantize(image_path, image_dst_path)

rmtree("./dist", ignore_errors=True)
makedirs("./dist/data", exist_ok=True)
makedirs("./dist/public/img/item", exist_ok=True)
shake("./data")
shake("./img")


with open("./order-item.txt", encoding="utf-8") as f:
  items_order = [*map(lambda s : s.strip(), f.readlines())]

items_order.reverse()

with open("./order-itemset.txt", encoding="utf-8") as f:
  itemsets_order = [*map(lambda s : s.strip(), f.readlines())]

itemsets_order.reverse()


item_files: list[str] = glob.glob("data/item/**/*.json", recursive=True)
itemset_files: list[str] = glob.glob("data/itemset/**/*.json", recursive=True)
image_files: list[str] = glob.glob("img/item/**/*.png", recursive=True)

image_hash: dict[str, str] = {}
for image_fname in image_files:
  image_key = splitext(basename(image_fname))[0]
  if image_key in image_hash:
    print(f"아이템 아이콘이 겹쳐요!: [{image_fname}] vs [{image_hash[image_key]}]")
  image_hash[image_key] = image_fname


items_array = []
for item_fname in item_files:
  item: dict = read_json(item_fname)
  pick_image(item, item_fname)
  
  items_array.append(item)

items_array.sort(key=indexy, reverse=True)
  

isets_array = []
for fname in itemset_files:
  iset: dict = read_json(fname)
  
  isets_array.append(iset)
  
isets_array.sort(key=iindexy, reverse=True)




# for i in image_files:
#   copy2(i, join("./dist/public/img/item", basename(i)))

with open("./dist/data/items.json", "w", encoding="utf-8") as write:
  json.dump(items_array, write, indent=None, separators=(",", ":"), ensure_ascii=False)

with open("./dist/data/itemsets.json", "w", encoding="utf-8") as write:
  json.dump(isets_array, write, indent=None, separators=(",", ":"), ensure_ascii=False)
