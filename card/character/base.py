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
    from entity.character import Character
    from entity.status import Status

    
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

    def __init__(self, from_character: Character) -> None:
        self.from_character: Character = from_character
    
    def generate_summon(self, game: GeniusGame):
        pass

    def calculate_dice_request(self, game: GeniusGame):
        # Equipment, Status, Talent(Yae Miko for e.g.) may save dice.
        pass

    def resolve_damage(self, game: GeniusGame, is_plunging_attack: bool=False, is_charged_attack: bool=False):
        Damage.resolve_damage(game, self.damage_type, self.main_damage_element, 
                              self.main_damage, self.piercing_damage, 
                              # TODO: 可能需要改一下调用的接口
                              self.from_character, get_opponent_active_character(game),
                              is_plunging_attack, is_charged_attack)
    def gain_energy(self, game: GeniusGame):
        pass

    def add_status(self, game: GeniusGame, status: Status):
        pass

    def on_call(self, game: GeniusGame):
        game.current_skill = self.type

class NormalAttack(CharacterSkill):

    def on_call(self, game: GeniusGame):
        super().on_call(game)
        # TODO: 判断是否为重击
        self.is_plunging_attack = False
        self.is_charged_attack = False

        # TODO: 消耗骰子
        self.calculate_dice_request(game)
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
        super().on_call(game)
        # TODO: Prepares for another Elemental Skill
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
        super().on_call(game)
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
        
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)




        
