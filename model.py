
from typing import Any, Literal, Optional, Union


def Item():
  def __init__(
    self, /, *,
    name: str,
    level: int,
    itype: str,
    rarity: Literal["Common", "Uncommon", "Rare", "Unique", "Epic"],
    image: Optional[str] = None,
    overlay: Optional[str] = None,
    setOf: Optional[Union[Literal["all"], list[str]]] = None,
    who: Optional[str] = None,
    content: Optional[list[str]] = None,
    part: Optional[str] = None,
    material: Optional[str] = None,
    ArtiColor: Optional[str] = None,
    attrs: dict = {},
    branch: Optional[list[dict]] = None,
    gives: Optional[list[dict]] = None,
    exclusive: Optional[list[dict]] = None
    ):
    self.name = name
    self.level = level
    self.itype = itype
    self.rarity = rarity
    self.image = image
    self.overlay = overlay
    self.setOf = setOf
    self.who = who
    self.content = content
    self.part = part
    self.material = material
    self.ArtiColor = ArtiColor
    self.attrs = attrs
    self.branch = branch
    self.gives = gives
    self.exclusive = exclusive