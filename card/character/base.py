from utils import *
from typing import List
from game.game import GeniusGame
from game.action import Action

class Damage:
    # 伤害基本类
    def __init__(self, damage_type, main_damage_element, main_damage, piercing_damage) -> None:
        self.damage_type: SkillType
        self.main_damage_element: ElementType = main_damage_element
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
    
    # damage
    damage_type: SkillType
    main_damage_element: ElementType
    main_damage: int
    piercing_damage: int

    # cost
    cost: list({'cost_num': int, 'cost_type': CostType})

    @classmethod
    def on_call(cls, game: GeniusGame, action: Action):
        
        # 消耗骰子
        # 降序排列以便于按索引pop
        for dice_index in sorted(action.dice, reverse=True):
            game.players[game.active_player].dice_zone.pop(dice_index)

        demage = Damage(cls.damage_type, cls.main_damage_element, cls.main_damage, cls.piercing_damage)
        
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


        
