from shutil import rmtree
from build_items import build_items

rmtree("./dist", ignore_errors=True)
build_items()
