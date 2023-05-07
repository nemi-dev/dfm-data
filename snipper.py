import json
import re
from src.read_json import read_json

z = {
  "천": "c",
  "가죽": "t",
  "경갑": "l",
  "중갑": "h",
  "판금": "p",
  
  "상의": "c",
  "하의": "p",
  "머리어깨": "n",
  "벨트": "b",
  "신발": "o"
}

def get_prefix(x: str):
  match = re.match(r"60에픽 ([^ ]+) ([^ ]+)", x)
  return z[match.group(1)] + z[match.group(2)]

bases = read_json("./armorbase.json")
snippet_list = {}

for item in bases:
  item_name = item["name"].replace("<", "").replace(">", "")
  material = item["material"]
  del item["material"]
  item["name"] = r"${0:$TM_FILENAME_BASE}"
  spec = {}
  body = json.dumps(item, indent=2, separators=(", ", ": "), ensure_ascii=False).split("\n")
  prefix = get_prefix(item_name)
  spec["prefix"] = prefix
  spec["scope"] = "json"
  spec["body"] = [*body]
  snippet_list[item_name] = spec
  
  spec_i = {}
  item_i = { **item }
  item_i["name"] = r"환(幻): ${0:iset} - "+item_i["itype"].replace("머리어깨", "어깨")
  item_i["material"] = material
  item_i["setOf"] = [r"환(幻): ${0:iset}"]
  item_i["image"] = "환영극단 "+ material + " " +item_i["itype"]
  
  spec_i["prefix"] = prefix + "i"
  spec_i["scope"] = "json"
  spec_i["body"] = json.dumps(item_i, indent=2, separators=(", ", ": "), ensure_ascii=False).split("\n")
  snippet_list[item_name + " : 환(幻)"] = spec_i
  
with open("60epic-armorbase.code-snippets", "w", encoding="utf-8") as w:
  json.dump(snippet_list, w, indent=2, separators=(", ", ": "), ensure_ascii=False)
