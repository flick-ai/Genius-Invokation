from genius_invocation.card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.event.damage import Damage
from genius_invocation.card.action.base import ActionCard
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
from genius_invocation.entity.character import Character
from genius_invocation.entity.status import Status, Combat_Status
from genius_invocation.entity.summon import Summon
from loguru import logger
import random

class Guhua_Style(NormalAttack):
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Guhua Style"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.HYDRO
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


class Fatal_Rainscreen(ElementalSkill):
    '''
    行秋
    元素战技
    '''
    id: int = 1
    name = "Stellar Restoration"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def add_status(self, game: 'GeniusGame'):
        char = get_my_active_character(game)
        status = self.from_character.from_player.team_combat_status.has_status(Rain_Sword)
        if status is None:
            status = Rain_Sword(game=game,
                    from_player=game.active_player,
                    from_character=char)
            self.from_character.from_player.team_combat_status.add_entity(status)
        else:
            status.update()

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        #附着水元素
        self.from_character.elemental_attach(game, ElementType.HYDRO)
        # 获得能量
        self.gain_energy(game)
        self.add_status(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Raincutter(ElementalBurst):
    '''
    行秋
    元素爆发
    '''
    id: int = 2
    name = "Fatal Rainscreen"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def add_status(self, game: 'GeniusGame'):
        status = self.from_character.from_player.team_combat_status.has_status(Rainbow_Bladework)
        if status is None:
            status = Rainbow_Bladework(game=game,
                    from_player=game.active_player,
                    from_character=self.from_character)
            self.from_character.from_player.team_combat_status.add_entity(status)
        else:
            status.update()

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.elemental_attach(game, ElementType.HYDRO)
        self.add_status(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Rain_Sword(Combat_Status):
    name = "Rain Sword"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.usage = 2
        if self.from_character.talent:
            self.max_usage = 3
            self.usage = 3

        self.current_usage = self.usage
    def update(self):
        if self.from_character.talent:
            self.max_usage = 3
            self.usage = 3
        self.current_usage = max(self.current_usage, self.usage)
    
    def on_excute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.damage_to.is_active:
                if game.current_damage.main_damage_element != ElementType.PIERCING:
                    if game.current_damage.main_damage >= 3:
                        game.current_damage.main_damage -= 1
                        self.current_usage -= 1
                        if self.current_usage <=0:
                            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXCUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_excute_dmg)
        ]

class Rainbow_Bladework(Combat_Status):
    name = "Rainbow Bladework"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.usage = 2
        self.current_usage = self.usage

    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game=game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.HYDRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()

                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Xingqiu(Character):
    id = 1202
    name = 'Xingqiu'
    element = ElementType.HYDRO
    weapon_type = WeaponType.SWORD
    country = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Guhua_Style, Fatal_Rainscreen, Raincutter]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0