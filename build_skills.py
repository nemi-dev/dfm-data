from src.data import getselfskill, getskill
from src.util import write_json

def build_skills():
  skills = getskill("")
  write_json(skills, "./dist/data/skills.json")
  
  selfskills = getselfskill("")
  write_json(selfskills, "./dist/data/selfskills.json")

if __name__ == "__main__":
  build_skills()
  