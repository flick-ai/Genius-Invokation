from utils import *
from typing import List, TYPE_CHECKING
from event.damage import Damage
from event.heal import Heal
from entity.entity import Entity


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

    def __init__(self, from_character: 'Character') -> None:
        self.from_character: Character = from_character
        self.is_plunging_attack: bool = False
        self.is_charged_attack: bool = False
        self.usage_this_round: int = 0

    def generate_summon(self, game: 'GeniusGame'):
        pass

    def consume_energy(self, game: 'GeniusGame'):
        pass

    def resolve_damage(self, game: 'GeniusGame'):
        game.add_damage(Damage.create_damage(game, self.damage_type, self.main_damage_element,
                              self.main_damage, self.piercing_damage,
                              # TODO: 可能需要改一下调用的接口
                              self.from_character, get_opponent_active_character(game),
                              self.is_plunging_attack, self.is_charged_attack))
        game.resolve_damage()
    def gain_energy(self, game: 'GeniusGame'):
        pass

    def add_status(self, game: 'GeniusGame'):
        pass

    def on_call(self, game: 'GeniusGame'):
        game.current_skill = self
        self.usage_this_round += 1

class NormalAttack(CharacterSkill):

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # TODO: 判断是否为重击
        self.is_plunging_attack = self.from_character.from_player.is_after_change
        self.is_charged_attack = self.from_character.from_player.dice_zone.dice_num % 2 == 0

        game.manager.invoke(EventType.ON_USE_SKILL, game)


class ElementalSkill(CharacterSkill):

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        
        game.manager.invoke(EventType.ON_USE_SKILL, game)


class ElementalBurst(CharacterSkill):

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        game.manager.invoke(EventType.ON_USE_SKILL, game)



# class PassiveSkill(CharacterSkill):


