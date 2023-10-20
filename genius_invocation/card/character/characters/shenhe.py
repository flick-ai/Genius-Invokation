from genius_invocation.card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.card.action.base import ActionCard
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.event.damage import Damage
from genius_invocation.entity.character import Character
from genius_invocation.entity.status import Status, Combat_Status
from genius_invocation.entity.summon import Summon
from loguru import logger

class Dawnstar_Piercer(NormalAttack):
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Dawnstar Piercer"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.CRYO
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


class Spring_Spirit_Summoning(ElementalSkill):
    id: int = 1
    name = "Spring Spirit Summoning"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
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
        self.add_combat_status(game, Icy_Quill)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Divine_Maidens_Deliverance(ElementalBurst):
    id = 2
    name = "Divine Maiden's Deliverance"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        self.generate_summon(game, Talisman_Spirit)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Shenhe(Character):
    id: int = 1107
    name = "Shenhe"
    element = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Dawnstar_Piercer, Spring_Spirit_Summoning, Divine_Maidens_Deliverance]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0

class Icy_Quill(Combat_Status):
    id: int = -1
    name: str = "Icy Quill"
    def __init__(self, game: 'GeniusGame', from_character: 'Character', from_player: 'GeniusPlayer'):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = 3
        self.max_usage = 3
        self.last_use_round = -1
    
    def update(self):
        self.current_usage = self.usage
    
    def on_dmg_add(self, game: 'GeniusGame'):
        if not isinstance(game.current_damage.damage_from, Character): return
        if game.current_damage.main_damage_element == ElementType.CRYO:
            if game.current_damage.damage_from.from_player == self.from_player:
                game.current_damage.main_damage += 1
                if self.from_character.talent and game.current_damage.damage_type==SkillType.NORMAL_ATTACK and self.last_use_round!= game.round:
                    self.last_use_round = game.round
                else:
                    self.current_usage -= 1
                    if self.current_usage <= 0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
           (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_dmg_add)
        ]


class Talisman_Spirit(Summon):
    name = "Talisman Spirit"
    element: ElementType = ElementType.CRYO
    usage: int = 2
    max_usage: int = 2
    removable = True

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.CRYO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from is not None:
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.main_damage_element == ElementType.CRYO or \
                        game.current_damage.main_damage_element == ElementType.PHYSICAL:
                    game.current_damage.main_damage_element += 1

    def update(self):
        self.current_usage = self.usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
            (EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.on_dmg_add)
        ]

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player=from_player, from_character=from_character)