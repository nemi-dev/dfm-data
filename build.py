from shutil import rmtree
from build_dfclass import build_dfclass
from build_items import build_items
from build_skills import build_skills

rmtree("./dist", ignore_errors=True)
build_dfclass()
build_items()
build_skills()
