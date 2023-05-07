from io import StringIO
from src.util import read_json

base_attrs_schema = read_json("./schema/base-attrs.json")

properties = base_attrs_schema["properties"]

buffer = StringIO()
buffer.write("| 키 | 설명 | 타입 | 단위 |\n")
buffer.write("| --- | --- | --- | --- |\n")

for key in properties:
  description = properties[key]["description"]
  _type = properties[key].get("type", "?")
  buffer.write(f"| {key} | {description} | {_type} |   |\n")

print(buffer.getvalue())
