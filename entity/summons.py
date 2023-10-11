from utils import *
from entity.entity import Entity


class Summon(Entity):
    # 召唤物基本类
    id: int
    name: str
    element: ElementType
    usage: int
    max_usage: int
    skills: list

    def __init__(self) -> None:
        self.usages: int # 此处是否需要区分青蛙和花鼠？
        # self.effect_text: str