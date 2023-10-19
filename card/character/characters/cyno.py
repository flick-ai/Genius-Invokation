from genius_invocation.card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from genius_invocation.entity.character import Character
from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.event.damage import Damage

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
from genius_invocation.entity.status import Status, Combat_Status
from loguru import logger

class Pactsworn_Pathclearer(Status):
    '''赛诺 被动状态'''
    name = "Pactsworn Pathclearer"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_level = 0
        self.max_level = 5
    
    def increase_level(self, level):
        self.current_level += level
        if self.current_level > self.max_level:
            self.current_level -= 4

    def on_end_phase(self, game:'GeniusGame'):
        self.increase_level(1)
    
    def infusion(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if self.current_level>=2:
                if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                    game.current_damage.main_damage_element = ElementType.ELECTRO
    
    def on_damage_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if self.current_level>=4:
                game.current_damage.main_damage += 2
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion)
        ]


class Invokers_Spear(NormalAttack):
    '''
    赛诺
    普通攻击
    '''
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Invokers Spear"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
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


class Secret_Rite_Chasmic_Soulfarer(ElementalSkill):
    '''
    赛诺
    元素战技
    '''
    id: int = 1
    name = "Secret Rite: Chasmic Soulfarer"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        if self.from_character.talent and self.from_character.character_zone.has_entity(Pactsworn_Pathclearer).current_level in [3,5]:
            self.resolve_damage(game, add_main_damage=1)
        else:
            self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Sacred_Rite_Wolfs_Swiftness(ElementalBurst):
    '''
    赛诺
    元素爆发
    '''
    id = 2
    name="Sacred Rite: Wolf's Swiftness"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.character_zone.has_entity(Pactsworn_Pathclearer).increase_level(2)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Cyno(Character):
    id = 1404
    name = "Cyno"
    element = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.SUNERU

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Invokers_Spear, Secret_Rite_Chasmic_Soulfarer, Sacred_Rite_Wolfs_Swiftness]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.character_zone.add_entity(Pactsworn_Pathclearer(game, self.from_player, self))

