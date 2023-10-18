from card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from entity.character import Character
from entity.entity import Entity
from entity.summon import Summon
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


class PrepareScissors(ElementalSkill):
    '''

    '''

class RockPaperScissorsCombo_Scissors(ElementalSkill):
    '''
        猜拳三连击·剪刀
    '''
    id: int = 12
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class RockPaperScissorsCombo_Paper(ElementalSkill):
    '''
        猜拳三连击·布
    '''
    id: int = 11
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


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

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.prepared_skill = 


class ChainsOfWardingThunder(Summon):
    '''
        雷锁镇域
    '''
    name: str = 'Oz'
    element: ElementType = ElementType.ELECTRO
    usage: int = 2
    max_usage: int = 2

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage
        self.used_this_round = True

class LightningLockdown(ElementalBurst):
    '''
        元素爆发
        雳霆镇锁
    '''
    id: int = 2
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ElectroCrystalCore(Status):
    '''
        雷晶核心
    '''
    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 1
            self.on_destroy(game)
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class ElectroHypostasis(Character):
    '''
        无相之雷
    '''
    id: int = 2401
    name: str = 'ElectroHypostasis'
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [ElectroCrystalProjection, RockPaperScissorsCambo, LightningLockdown]

    max_power: int = 2

    def init_state(self, game: GeniusGame):
        '''
            被动技能: 战斗开始时, 初始附属雷晶核心
        '''
        electro_crystal_core = ElectroCrystalCore(game=game,
                                                  from_player=self.from_player,
                                                  from_character=self)
        self.character_zone.add_entity(electro_crystal_core)

    def __init__(self, game: 'GeniusGame', character_zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, character_zone, from_player, index, from_character)
        self.talent = talent
        self.prepared_skill = None