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
class Yuuban_Meigen(NormalAttack):
    id: int = 0
    name = "Yuuban Meigen"
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ANEPMO
    main_damage: int = 1
    piercing_damage = 0

    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ANEPMO
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
        
        
        self.resolve_damage(game)

        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Hanega_Song_of_the_Wind(ElementalSkill):
    id = 1
    name = "Hanega: Song of the Wind"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEPMO
    main_damage: int = 2
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEPMO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)
    
    def add_status(self, game: 'GeniusGame'):
        status = self.from_character.character_zone.has_entity(Windfavored)
        if status is None:
            status = Windfavored(game, self.from_character.from_player, self.from_character)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.add_status(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Kyougen_Five_Ceremonial_Plays(ElementalBurst):
    id = 2
    name = "Kyougen: Five Ceremonial Plays"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEPMO
    main_damage: int = 7
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEPMO
        },
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)
    
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Wanderer(Character):
    id = 1506
    name = "Wanderer"
    element = ElementType.ANEPMO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.OTHER

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Yuuban_Meigen, Hanega_Song_of_the_Wind, Kyougen_Five_Ceremonial_Plays]

    max_power = 3

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0

class Windfavored(Status):
    '''
    优风倾姿
    '''
    name = "Windfavored"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character') -> None:
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2
    
    def update(self):
        self.current_usage = self.usage
    
    def on_dmg_add(self, game: 'GeniusGame') :
        # logger.debug(game.current_damage.damage_from.name)
        # logger.debug(self.from_character.name)
        if game.current_damage.damage_from != self.from_character:
            return
        if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
            game.current_damage.main_damage += 2
            target = get_opponent_active_character(game)
            ls = get_opponent_standby_character(game)
            if len(ls)>0:
                target = ls[0]
            game.current_damage.damage_to = target

            if self.from_character.talent and game.current_damage.is_charged_attack:
                status = self.from_character.character_zone.has_entity(Switch)
                if status is None:
                    status = Switch(game, self.from_player, self.from_character)
                    self.from_character.character_zone.add_entity(status)
                else:
                    status.update()

            self.current_usage -= 1
        elif game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
            game.current_damage.main_damage += 1
            self.current_usage = 0

        if self.current_usage <= 0:
            self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]

class Switch(Status):
    '''
    Talent effect
    '''
    #TODO: Check whether passive switch triggers this status?
    name = "Switch_From_Wanderer"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character') -> None:
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.max_usage = 1
        self.current_usage = 1
    
    def update(self):
        self.current_usage = self.usage

    def on_switch(self, game: 'GeniusGame'):
        if game.active_player != self.from_player: return
        if game.active_player.active_idx != self.from_character.index: return
        if game.current_dice.use_type == "change_character":
            if game.current_dice.cost[0]['cost_num']>0:
                game.current_dice.cost[0]['cost_num'] -=1
            
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
                main_damage=1,
                main_damage_element=ElementType.ANEPMO,
                piercing_damage=0
            )
            game.add_damage(dmg)
            game.resolve_damage()

            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch)
        ]

            