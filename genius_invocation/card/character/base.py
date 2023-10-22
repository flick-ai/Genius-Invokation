from genius_invocation.utils import *
from typing import List, TYPE_CHECKING
from genius_invocation.event.damage import Damage
from genius_invocation.event.heal import Heal
from genius_invocation.entity.entity import Entity

from loguru import logger


if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.entity.character import Character
    from genius_invocation.entity.status import Status


class CharacterSkill:
    # 角色技能基本类
    id: int
    name: str
    name_ch: str = ""
    type: SkillType

    # damage
    damage_type: SkillType
    main_damage_element: ElementType
    main_damage: int
    piercing_damage: int

    # cost
    cost: list({'cost_num': int, 'cost_type': CostType})
    energy_cost: int
    energy_gain: int

    def __init__(self, from_character: 'Character') -> None:
        self.from_character: Character = from_character
        self.is_plunging_attack: bool = False
        self.is_charged_attack: bool = False
        self.usage_this_round: int = 0

    def consume_energy(self, game: 'GeniusGame'):
        assert self.from_character.power >= self.energy_cost
        self.from_character.power -= self.energy_cost

    def resolve_damage(self, game: 'GeniusGame', add_main_damage:int = 0, add_piercing_damage:int = 0):
        game.add_damage(Damage.create_damage(game, self.damage_type, self.main_damage_element,
                              self.main_damage + add_main_damage,
                              self.piercing_damage + add_piercing_damage,
                              # TODO: 可能需要改一下调用的接口
                              self.from_character, get_opponent_active_character(game),
                              self.is_plunging_attack, self.is_charged_attack))
        game.resolve_damage()
    def gain_energy(self, game: 'GeniusGame'):
        self.from_character.power += self.energy_gain
        self.from_character.power = min(self.from_character.power, self.from_character.max_power)

    def add_status(self, game: 'GeniusGame', STATUS): 
        # Add a status in character zone of current character
        # Here status is the "class" of status, is not an instance of status
        status = self.from_character.character_zone.has_entity(STATUS)
        if status is None:
            status = STATUS(game, self.from_character.from_player, self.from_character)
            self.from_character.character_zone.add_entity(status)
        else:
            try:
                status.update(game)
            except:
                status.update()

    def add_shield(self, game: 'GeniusGame', SHIELD):
        # Add a shield in character zone of current character
        # Here SHIELD is the "class" of shield, is not an instance of shield
        shield = self.from_character.character_zone.has_entity(SHIELD)
        if shield is None:
            shield = SHIELD(game, self.from_character.from_player, self.from_character)
            self.from_character.character_zone.add_entity(shield)
        else:
            try:
                shield.update(game)
            except:
                shield.update()

    def add_combat_status(self, game: 'GeniusGame', STATUS):
        # Add a combat status in active zone of current player
        # Here STATUS is the "class" of Combat_Status, is not an instance of status
        status = self.from_character.from_player.team_combat_status.has_status(STATUS)
        if status is None:
            status = STATUS(game, self.from_character.from_player, self.from_character)
            self.from_character.from_player.team_combat_status.add_entity(status)
        else:
            try:
                status.update(game)
            except:
                status.update()

    def generate_summon(self, game: 'GeniusGame', SUMMON):
        # Add a summon in summons zone of current player
        # Here SUMMON is the "class" of SUMMON, is not an instance of status
        summon = self.from_character.from_player.summon_zone.has_entity(SUMMON)
        if summon is None:
            summon = SUMMON(game, self.from_character.from_player, self.from_character)
            self.from_character.from_player.summon_zone.add_entity(summon)
        else:
            try:
                summon.update(game)
            except:
                summon.update()
    
    def add_combat_shield(self, game: 'GeniusGame', COMBAT_SHIELD):
        # Add a combat shield in active zone of current player
        # Here COMBAT_SHIELD is the "class" of Combat_Shield, is not an instance
        shield = self.from_character.from_player.team_combat_status.has_shield(COMBAT_SHIELD)
        if shield is None:
            shield = COMBAT_SHIELD(game, self.from_character.from_player, self.from_character)
            self.from_character.from_player.team_combat_status.add_entity(shield)
        else:
            try:
                shield.update(game)
            except:
                shield.update()
    # MORE ADD SITUATION NEED TO IMPLEMENT IN THE SUBCLASS.
    def before_use_skill(self, game: 'GeniusGame'):
        pass

    def on_call(self, game: 'GeniusGame'):
        game.current_skill = self
        self.usage_this_round += 1

class NormalAttack(CharacterSkill):

    def before_use_skill(self, game: 'GeniusGame'):
        self.is_plunging_attack = self.from_character.from_player.is_after_change
        self.is_charged_attack = self.from_character.from_player.dice_zone.dice_num % 2 == 0
        logger.info(f'is_plunging_attack: {self.is_plunging_attack}')
        logger.info(f'is_charged_attack: {self.is_charged_attack}')

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # TODO: 判断是否为重击
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


