'''
Implements of Elemental Reaction.
No Damage Calculation.
All the player_id here is the player who has reaction on his character.
'''
from typing import TYPE_CHECKING
from genius_invocation.card.character.base import *

from genius_invocation.entity.status import *
from genius_invocation.entity.summon import *
from loguru import logger
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


#The Elemental Reaction always with the first attached element.
def Frozen(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx]
    '''
    # game.players[player_id].character_list[target_idx].character_zone.is_frozen = True
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    status = game.players[player_id].character_list[target_idx].character_zone.has_entity(Frozen_Status)
    if status is None:
        game.players[player_id].character_list[target_idx].character_zone.add_entity(Frozen_Status(game, game.players[player_id], game.players[player_id].character_list[target_idx]))
    logger.info("Trigger Elemental_Reaction: Frozen")
def Melt(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    logger.info("Trigger Elemental_Reaction: Melt")


def Vaporize(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    logger.info("Trigger Elemental_Reaction: Vaporize")

def Superconduct(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    logger.info("Trigger Elemental_Reaction: Superconduct")

def Electro_Charged(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    logger.info("Trigger Elemental_Reaction: Electro Charged")

def Bloom(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)

    special_status = game.players[1-player_id].team_combat_status.has_status(GoldenChalice)
    if special_status is None:
        status = game.players[1-player_id].team_combat_status.has_status(Dendro_Core)
        if status is not None:
            status.update()
        else:
            game.players[1-player_id].team_combat_status.add_entity(Dendro_Core(game, game.players[1-player_id], None))
        logger.info("Trigger Elemental_Reaction: Bloom")
    else:
        summon = game.players[1-player_id].summon_zone.has_entity(BountifulCore)
        if summon is not None:
            summon.update()
        else:
            game.players[1-player_id].summon_zone.add_entity(BountifulCore(game, game.players[1-player_id], None))
        logger.info("Trigger Elemental_Reaction: Special Bloom")

def Overloaded(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    # game.players[player_id].change_to_next_character()
    logger.info("Trigger Elemental_Reaction: Overloaded")


def Burning(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    summon = game.players[1-player_id].summon_zone.has_entity(Burning_Flame)
    if summon is not None:
        summon.update()
    else:
        game.players[1-player_id].summon_zone.add_entity(Burning_Flame(game, game.players[1-player_id], None))
    logger.info("Trigger Elemental_Reaction: Burning")

def Quicken(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)

    status = game.players[1-player_id].team_combat_status.has_status(Catalyzing_Feild)
    if status is None:
        game.players[1-player_id].team_combat_status.add_entity(Catalyzing_Feild(game, game.players[1-player_id], None))
    else:
        status.update()

    logger.info("Trigger Elemental_Reaction: Quicken")
def Swirl(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    logger.info("Trigger Elemental_Reaction: Swirl")


def Crystallize(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].elemental_application.pop(0)
    status = game.players[1-player_id].team_combat_status.has_shield(Crystallize_Shield)
    if status is not None:
        status.update()
    else:
        game.players[1-player_id].team_combat_status.add_entity(Crystallize_Shield(game, game.players[1-player_id], None))
    logger.info("Trigger Elemental_Reaction: Crystallize")
