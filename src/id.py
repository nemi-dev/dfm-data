from hashlib import sha256

hashmap: dict[int, str] = {}

def genid(s: str):
  bin = s.encode()
  digest = sha256(bin).digest()
  a, b, c, d = map(lambda i : int.from_bytes(digest[i * 4 : (i + 1) * 4]), range(0, 4))
  num = a ^ b ^ c ^ d
  while num in hashmap:
    if hashmap[num] == s:
      return num
    num += 1
  hashmap[num] = s
  return num
