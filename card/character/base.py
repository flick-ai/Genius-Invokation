from utils import *
from typing import List
from game.game import GeniusGame

class Damage:
    # 伤害基本类
    def __init__(self, main_damage_type, main_damage, piercing_damage) -> None:
        self.main_damage_type: ElementType = main_damage_type
        self.main_damage: int = main_damage
        self.piercing_damage: int = piercing_damage
    

class Summon:
    # 召唤物基本类
    def __init__(self) -> None:
        self.usages: int # 此处是否需要区分青蛙和花鼠？
        self.effect: str

class CharacterSkill:
    # 角色技能基本类
    id: int
    name: str
    type: SkillType
    demage: Damage
        
class CharacterCard:
    # 角色卡片基本类
    id: int
    name: str
    element: ElementType
    weapon_type: WeaponType
    country: CountryType
    health_point: int
    skills: {'Normal Attack':CharacterSkill, 'Elemental Skill':CharacterSkill, 'Elemental Burst':CharacterSkill, 'Passive Skill':CharacterSkill}
    power: int
    max_power: int
    # def __init__(self) -> None:

    
    def use_skill(self):
        pass


        
