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

class Majestic_Dance(NormalAttack):
    id: int = 0
    name = "Majestic Dance"
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.DENDRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Volatile_Spore_Cloud(ElementalSkill):
    id = 1
    name = "Volatile Spore Cloud"
    type = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)

        if self.from_character.talent:
            self.from_character.character_zone.has_entity(Radical_Vitality).equip_talent()
            # TODO: when add talent card, add this statement to that on_call, And Remove it.
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Feather_Spreading(ElementalBurst):
    name = "Feather Spreading"
    id = 2
    type = SkillType.ELEMENTAL_BURST

    damage_type = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.DENDRO
    main_damage = 4
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
        }
    ]
    energy_cost = 2
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        status = self.from_character.character_zone.has_entity(Radical_Vitality)
        addition_dmg = status.current_usage
        status.current_usage = 0
        self.resolve_damage(game, add_main_damage=addition_dmg)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class Jadeplume_Terrorshroom(Character):
    id = 2701
    name = "Jadeplume Terrorshroom"
    element = ElementType.DENDRO
    weapon_type = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER

    init_health_point = 10
    max_health_point = 10
    skill_list = [Majestic_Dance, Volatile_Spore_Cloud, Feather_Spreading]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent

    def init_state(self, game: 'GeniusGame'):
        self.character_zone.add_entity(Radical_Vitality(game, self.from_player, self))

    def revive(self, game: 'GeniusGame'):
        super().revive(game)
        self.init_state(game)

class Radical_Vitality(Status):
    name = "Radical Vitality"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 3
        self.current_usage = 0
        if self.from_character.talent:
            self.max_usage = 4

    def equip_talent(self):
        self.max_usage = 4

    def update(self): #No update
        pass

    def on_excute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.main_damage_element in [ElementType.PHYSICAL, ElementType.PIERCING]:
            return

        if game.current_damage.damage_from == self.from_character or game.current_damage.damage_to == self.from_character:
            self.current_usage += 1
            if self.current_usage >self.max_usage:
                self.current_usage = self.max_usage
    
    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            if self.current_usage == self.max_usage:
                self.current_usage = 0
                self.from_character.power = 0
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXCUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_excute_dmg),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]
            

