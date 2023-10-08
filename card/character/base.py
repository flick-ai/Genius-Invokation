from utils import *
from typing import List
from game.game import GeniusGame

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
        self.type: SkillType
        self.name: str
        self.demage: Damage
        
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

class ActionCard:
    # 行动牌基本类
    def __init__(self) -> None:
        self.id: int
        self.name: str

    def on_played(self, game: GeniusGame) -> None:
        raise NotImplementedError


class EquipmentCard(ActionCard):
    # 装备牌基本类
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame, target) -> None:
        pass


class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()

        
