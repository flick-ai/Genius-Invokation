'''
Implements of Elemental Reaction.
No Damage Calculation.
All the player_id here is the player who has reaction on his character.
'''
from typing import TYPE_CHECKING
from card.character.base import *

from entity.status import *
from entity.summon import *

if TYPE_CHECKING:
    from game.game import GeniusGame


#The Elemental Reaction always with the first attached element.
def Frozen(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx]
    '''
    # game.players[player_id].character_list[target_idx].character_zone.is_frozen = True
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    status = game.players[player_id].character_list[target_idx].character_zone.has_entity(Frozen_Status)
    if status is None:
        game.players[player_id].character_list[target_idx].character_zone.add_entity(Frozen_Status(game, game.players[player_id], game.players[player_id].character_list[target_idx]))

def Melt(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)

def Vaporize(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)

def Superconduct(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    
def Electro_Charged(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    
def Bloom(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    
    status = game.players[1-player_id].team_combat_status.has_status(Dendro_Core)
    if status is not None:
        status.update()
    else:
        game.players[1-player_id].team_combat_status.add_entity(Dendro_Core(game, game.players[1-player_id], None))

def Overloaded(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    game.players[player_id].change_to_next_character()

def Burning(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    summon = game.players[1-player_id].summons_zone.has_entity(Burning_Flame)
    if summon is not None:
        summon.update()
    else:
        game.players[1-player_id].summons_zone.add_entity(Burning_Flame(game, game.players[1-player_id], None))

def Quicken(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    
    status = game.players[1-player_id].team_combat_status.has_status(Catalyzing_Feild)
    if status is None:
        game.players[1-player_id].team_combat_status.add_entity(Catalyzing_Feild(game, game.players[1-player_id], None))
    else:
        status.update()


def Swirl(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)


def Crystallize(game: 'GeniusGame', player_id: int, target_idx: int):
    '''
    game.players[player_id].active_zone.character_list[target_idx] .
    '''
    game.players[player_id].character_list[target_idx].character_zone.elemental_application.pop(0)
    status = game.players[1-player_id].team_combat_status.has_shield(Crystallize_Shield)
    if status is not None:
        status.update()
    else:
        game.players[1-player_id].team_combat_status.add_entity(Crystallize_Shield(game, game.players[1-player_id], None))
