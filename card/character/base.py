from utils import *
from typing import List

class Damage:
    # 伤害基本类
    def __init__(self) -> None:
        self.main_damage_type: ElementType
        self.main_damage: int
        self.piercing_damage: int 
    

class Summon:
    # 召唤物基本类
    def __init__(self) -> None:
        self.usages: int # 此处是否需要区分青蛙和花鼠？
        self.effect: str

class CharacterSkill:
    # 角色技能基本类
    def __init__(self) -> None:
        pass
        
class CharacterCard:
    # 角色卡片基本类
    def __init__(self) -> None:
        self.id: int
        self.name: str
        self.element: ElementType
        self.weapon_type: WeaponType
        self.country: CountryType
        self.health_point: int
        self.skills: {'Normal Attack':CharacterSkill, 'Elemental Skill':CharacterSkill, 'Elemental Burst':CharacterSkill, 'Passive Skill':CharacterSkill}
        self.power: int
        self.max_power: int
    
    def use_skill(self):
        pass
        
