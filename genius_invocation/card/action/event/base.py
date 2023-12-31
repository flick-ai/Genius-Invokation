from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Satisfy_Statue
from genius_invocation.utils import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class FoodCard(ActionCard):
    id: int
    name: str
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT_FOOD

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        if game.current_action.target_type == ActionTarget.MY_CHARACTER:
            target = game.current_action.target_idx
            target_character = game.active_player.character_list[target]
            satisfy = Satisfy_Statue(game, from_player=game.active_player, from_character=target_character)
            target_character.character_zone.add_entity(satisfy)
            if self.food_entity != None:
                target_character.character_zone.add_entity(self.food_entity(game, from_player=game.active_player, from_character=target_character))
            return target_character
        else:
            for character in game.active_player.character_list:
                if not character.is_satisfy:
                    satisfy = Satisfy_Statue(game, from_player=game.active_player, from_character=character)
                    character.character_zone.add_entity(satisfy)
                    if self.food_entity != None:
                        target_character.character_zone.add_entity(self.food_entity(game, from_player=game.active_player, from_character=target_character))

    def find_target(self, game: 'GeniusGame'):
        target_list = []
        for idx, character in enumerate(game.active_player.character_list):
            if not character.is_satisfy and character.is_alive:
                target_list.append(idx+2)
        return target_list
