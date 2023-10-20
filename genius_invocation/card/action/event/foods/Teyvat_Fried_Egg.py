from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status, Satisfy_Statue
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class NoRevie(Status):
    id: int = 333009
    name: str = "No Revive"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

class Teyvat_Fried_Egg(FoodCard):
    id: int = 333009
    name: str = "Teyvat Fried Egg"
    cost_num = 2
    cost_type = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = NoRevie

    def on_played(self, game: 'GeniusGame'):
        target = game.current_action.target_idx
        target_character = game.active_player.character_list[target]
        target_character.revive(game)
        Satisfy_Statue(game, from_player=game.active_player, from_character=target_character)
        target_character.character_zone.add_entity(Satisfy_Statue)
           
        game.active_player.team_combat_status.add_entity(self.food_entity(game, from_player=game.active_player, from_character=target_character))
    
    def find_target(self, game: 'GeniusGame'):
        target_list = []
        status = game.active_player.team_combat_status.has_status(NoRevie)
        if status is None:
            for idx, character in enumerate(game.active_player.character_list):
                if not character.is_alive:
                    target_list.append(idx+2)
        return target_list
    