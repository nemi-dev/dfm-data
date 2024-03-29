from base64 import b64encode
from glob import glob
from hashlib import sha224
from os.path import basename, exists, join, splitext
from sys import stderr

from PIL import Image

from .util import sanitize_filename, shake

with open("path-to-img.txt", encoding="UTF-8") as r:
  path_to_img = r.read().strip()
  GLOB_IMG = join(path_to_img, "item/**/*.png")
  
shake("./data")
shake(path_to_img)

digest_table: dict[int, str] = {}
case_sensitive_table: dict[str, str] = {}

  
image_files: list[str] = glob(GLOB_IMG, recursive=True)
image_basename_path_map: dict[str, str] = {}

for image_fname in image_files:
  image_basename = splitext(basename(image_fname))[0]
  if image_basename in image_basename_path_map:
    print(f"아이템 아이콘이 겹쳐요!: [{image_fname}] vs [{image_basename_path_map[image_basename]}]")
  image_basename_path_map[image_basename] = image_fname

def quantize(input_img_path: str, output_img_path: str):
  with Image.open(input_img_path) as im:
    im_p = im.resize((64, 64)).quantize(256)
    im_p.save(output_img_path)

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


def pick_image(item: dict):
  name: str = item["name"]
  image_key_to_find = item.get("image", sanitize_filename(name))
  if not (image_key_to_find in image_basename_path_map):
    return print(f"아이템({item['name']})에 적절한 그림이 없어요!", file=stderr)
  
  image_digest = sha224(image_key_to_find.encode()).digest()
  image_dst = fold(image_digest, image_key_to_find).decode()
  item["image"] = image_dst
  if image_dst.lower() in case_sensitive_table:
    if case_sensitive_table[image_dst.lower()] != image_key_to_find:
      print("이미지 파일 해시가 겹쳐요!!", file=stderr)
  case_sensitive_table[image_dst.lower()] = image_key_to_find

  image_path = image_basename_path_map[image_key_to_find]
  image_dst_path = join("./dist/public/img/item", image_dst + ".png")
  if not exists(image_dst_path):
    quantize(image_path, image_dst_path)
    