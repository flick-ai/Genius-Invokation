from game.game import GeniusGame
from utils import *
from typing import List, TYPE_CHECKING
from event.damage import Damage
from event.heal import Heal
from entity.entity import Entity
from utils import GeniusGame


if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode
    from entity.character import CharacterCard

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

    # heal
    heal: int

    # cost
    cost: list({'cost_num': int, 'cost_type': CostType})
    energy_cost: int
    energy_gain: int

    def __init__(self, from_character: CharacterCard) -> None:
        self.from_character: CharacterCard = from_character
    
    def generate_summon(self, game: GeniusGame):
        pass

    def on_call(self, game: GeniusGame):
        pass

class NormalAttack(CharacterSkill):

    def on_call(self, game: GeniusGame):

        # TODO: 判断是否为重击
        is_plunging_attack = False
        is_charged_attack = False
        game.manager.invoke('before_skill', game)

        # TODO: 消耗骰子
        # TODO: 判断技能是否有伤害
        # 伤害执行
        Damage.resolve_damage(game, self.damage_type, self.main_damage_element, 
                              self.main_damage, self.piercing_damage, 
                              # TODO: 可能需要改一下调用的接口
                              self.from_character, get_opponent_active_character(game),
                              is_plunging_attack, is_charged_attack)

        # 治疗执行

        # TODO: 获得能量
        
        game.manager.invoke('after_skill', game)


class ElementalSkill(CharacterSkill):

    def on_call(self, game: GeniusGame):

        game.manager.invoke('before_skill', game)

        # TODO: 消耗骰子
        # TODO: 判断技能是否有伤害
        # 伤害执行
        Damage.resolve_damage(game, self.damage_type, self.main_damage_element, 
                              self.main_damage, self.piercing_damage,
                              # TODO: 可能需要改一下调用的接口
                              self.from_character, get_opponent_active_character(game),)

        # 治疗执行

        # 召唤物/状态生成
        self.generate_summon(game)

        # TODO: 获得能量
        
        game.manager.invoke('after_skill', game)


class ElementalBurst(CharacterSkill):

    def on_call(self, game: GeniusGame):

        game.manager.invoke('before_skill', game)

        # TODO: 消耗骰子
        # TODO: 消耗能量

        # TODO: 判断技能是否有伤害
        # 伤害执行
        Damage.resolve_damage(game, self.damage_type, self.main_damage_element, 
                              self.main_damage, self.piercing_damage,
                              # TODO: 可能需要改一下调用的接口
                              self.from_character, get_opponent_active_character(game),)

        # 治疗执行

        # 召唤物/状态生成
        self.generate_summon(game)
        
        game.manager.invoke('after_skill', game)




        
