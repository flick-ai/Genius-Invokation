from card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from entity.character import Character
from entity.entity import Entity
from utils import *
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode
    from game.player import GeniusPlayer
    from event.damage import Damage
    from game.zone import CharacterZone

from entity.status import Status

class ElectroCrystalProjection(NormalAttack):
    '''
        雷晶投射
    '''
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ELECTRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class RockPaperScissorsCombo_Scissors(ElementalSkill):
    pass


class RockPaperScissorsCambo(ElementalSkill):
    '''
        猜拳三连击
    '''
    id: int = 1
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 5,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1



class ElectroHypostasis(Character):
    '''

    '''
    id: int = 2401
    name: str = 'ElectroHypostasis'
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [NormalAttack, ElementalSkill, ElementalBurst]

    power: int = 0
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', character_zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, character_zone, from_player, index, from_character)
        self.talent = talent