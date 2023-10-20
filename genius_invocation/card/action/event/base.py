from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Satisfy_Statue
from utils import *
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
        self.food_entity
    
    def on_played(self, game: 'GeniusGame') -> None:
        if game.current_action.target_ty == ActionTarget.MY_CHARACTER:
            target = game.current_action.target_idx
            target_character = game.active_player.character_list[target]
            Satisfy_Statue(game, from_player=game.active_player, from_character=target_character)
            target_character.character_zone.add_entity(Satisfy_Statue)
            target_character.character_zone.add_entity(self.food_entity(game, from_player=game.active_player, from_character=target_character))

    def find_target(self, game: GeniusGame):
        target_list = []
        for idx, character in enumerate(game.active_player.character_list):
            if not character.is_satisfy:
                target_list.append(idx+2)
        return target_list
