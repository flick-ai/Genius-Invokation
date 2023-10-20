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

class Fight_Club_Legend(NormalAttack):
    id: int = 0
    name = "Bolts of Downfall"
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
            'cost_type': CostType.GEO
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

class Masatsu_Zetsugi_Akaushi_Burst(ElementalSkill):
    id = 1
    name = "Masatsu Zetsugi: Akaushi Burst"
    type = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.GEO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def generate_summon(self, game: 'GeniusGame'):
        '''
            生成牛牛
        '''
        summon = self.from_character.from_player.summons_zone.has_entity(Ushi)
        if summon is None:
            summon = Ushi(game=game,
                    from_player=self.from_character.from_player,
                    from_character=self.from_character)
            self.from_character.from_player.summons_zone.add_entity(summon)
        else:
            summon.update()

    def add_status(self, game: 'GeniusGame'):
        status = self.from_character.character_zone.has_entity(Superlative_Superstrength)
        if status is None:
            status = Superlative_Superstrength(game, self.from_character.from_player, self.from_character)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.generate_summon(game)
        self.add_status(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Royal_Descent_Behold_Itto_the_Evil(ElementalBurst):
    name = 'Royal Descent: Behold, Itto the Evil!'
    id = 2
    type = SkillType.ELEMENTAL_BURST

    damage_type = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.GEO
    main_damage = 5
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.GEO
        }
    ]
    energy_cost = 3
    energy_gain = 0

    def add_status(self, game: 'GeniusGame'):
        status = self.from_character.character_zone.has_entity(Raging_Oni_King)
        if status is None:
            status = Raging_Oni_King(game, self.from_character.from_player, self.from_character)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_status(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Arataki_Itto(Character):
    id: int = 1605
    name: str = 'Arataki Itto'
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [
        Fight_Club_Legend,
        Masatsu_Zetsugi_Akaushi_Burst,
        Royal_Descent_Behold_Itto_the_Evil
    ]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent

class Ushi(Summon):
    '''牛牛'''
    name = 'Ushi'
    element = ElementType.GEO
    usage = 1
    removable = False
    max_usage = 1

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            
            status = self.from_player.team_combat_status.has_status(Shield_from_Ushi)
            if status is not None:
                status.on_destroy(game)
            self.on_destroy(game)
    
    def after_take_dmg(self, game: 'GeniusGame'):
        if self.add_strength: return
        if game.current_damage.damage_to.from_player == self.from_player:
            self.add_strength = True
            status = self.from_character.character_zone.has_entity(Superlative_Superstrength)
            if status is not None:
                status.update()
            else:
                status = Superlative_Superstrength(game, self.from_player, self.from_character)
                self.from_character.character_zone.add_entity(status)

    def update(self, game:'GeniusGame'):
        if self.current_usage == 0:
            self.current_usage = self.usage
            assert self.from_player.team_combat_status.has_status(Shield_from_Ushi) is None
            status = Shield_from_Ushi(game, self.from_player, self.from_character, self)
            self.from_player.team_combat_status.add_entity(status)
        else:
            pass
            #No Need to Update            
        self.add_strength = False

    def add_usage(self, game: 'GeniusGame', count: int):
        self.current_usage += count
        if self.current_usage == count:
            status = Shield_from_Ushi(game, self.from_player, self.from_character, self)
            self.from_player.team_combat_status.add_entity(status)
       
        self.from_player.team_combat_status.has_status(Shield_from_Ushi).update()

    def minus_usage(self, game: 'GeniusGame', count: int):
        if self.current_usage == 0: return
        self.current_usage -= count
        self.current_usage = max(0, self.current_usage)
        if self.current_usage == 0:
            self.from_player.team_combat_status.has_status(Shield_from_Ushi).on_destroy(game)
    
    def on_destroy(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(Shield_from_Ushi)
        if status is not None:
            status.on_destroy(game)
        super().on_destroy(game)

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage
        self.add_strength = False
        assert self.from_player.team_combat_status.has_status(Shield_from_Ushi) is None
        status = Shield_from_Ushi(game, self.from_player, self.from_character, self)
        self.from_player.team_combat_status.add_entity(status)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end_phase),
            (EventType.AFTER_TAKES_DMG, ZoneType.ACTIVE_ZONE, self.after_take_dmg),
        ]

class Shield_from_Ushi(Combat_Status):
    name = 'Shield from Ushi'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, from_summon:'Summon' = None):
        super().__init__(game, from_player, from_character)
        # USAGE SHOULD ALWAYS SAME WITH SUMMON
        self.from_summon = from_summon
        self.current_usage = self.from_summon.current_usage
        self.usage = self.from_summon.usage
        self.max_usage = self.from_summon.max_usage

    def on_damage_excute(self, game:'GeniusGame'):
        if self.from_summon.current_usage <=0: return
        if game.current_damage.main_damage <=0: return
        if game.current_damage.main_damage_element==ElementType.PIERCING: return
        if game.current_damage.damage_to.from_player == self.from_player:
            game.current_damage.main_damage -= 1
            self.from_summon.current_usage -= 1
            self.current_usage = self.from_summon.current_usage
            if self.from_summon.current_usage ==0:
                self.on_destroy(game) # Only destroy the combat_status here
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXCUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_damage_excute)
        ]
    def update(self):
        self.current_usage = self.from_summon.current_usage

class Raging_Oni_King(Status):
    '''怒目鬼王'''
    name = "Raging Oni King"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.usage = 2
        self.current_usage = 2
        self.current_round = -1

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)
    
    def after_skill(self, game:"GeniusGame"):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                if game.round != self.current_round:
                    self.current_round = game.round
                    status = self.from_character.character_zone.has_entity(Superlative_Superstrength)
                    if status is not None:
                        status.update()
                    else:
                        status = Superlative_Superstrength(game, self.from_player, self.from_character)
                        self.from_character.character_zone.add_entity(status)
    def infusion(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.GEO
    
    def on_dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.main_damage += 2
    
    def on_begin_phase(self, game:'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase)
        ]



class Superlative_Superstrength(Status):
    '''乱神之怪力'''
    name = "Superlative Superstrength"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 3
        self.usage = 1
        self.current_usage = 1
    
    def update(self):
        self.current_usage = min(self.max_usage, self.current_usage + self.usage)
    
    def on_calculation(self, game:"GeniusGame"):
        if self.current_usage<2: return False
        if self.from_player.dice_zone.num()%2!=0: return False
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type is SkillType.NORMAL_ATTACK: 
                if game.current_dice.from_character == self.from_character:  #Ito use normal attack, Ito
                    if self.usage > 0:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type is ActionCardType.EQUIPMENT_TALENT:
                    if self.usage > 0:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False
                    
    def on_skill(self, game:"GeniusGame"):
        self.on_calculation(game)
            
    def on_dmg_add(self, game:"GeniusGame"):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                if game.current_damage.is_charged_attack:
                    if self.from_character.talent:
                        if game.current_skill.usage_this_round >=2:
                            game.current_damage.main_damage += 1
                    game.current_damage.main_damage += 1
                    self.current_usage -= 1
                    if self.current_usage <=0:
                        self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculation)
        ]