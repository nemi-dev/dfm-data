from src.data import *

for item in dfitems():
  if "exclusive" in item:
    exclusive: list[dict] = item["exclusive"]
    # print(exclusive)
    for exclusiveSet in exclusive:
      # print(exclusiveSet)
      if "name" in exclusiveSet:
        print(item["name"], "의 exclusiveSet ID 속성명이 name이에욧!!!")
      if "label" in exclusiveSet:
        print(item["name"], "의 exclusiveSet에 label이 있어욧!!!!")
        
      for node in exclusiveSet:
        if "name" in node:
          print(item["name"], "의 exclusive child ID 속성명이 name이에욧!!!")
        
