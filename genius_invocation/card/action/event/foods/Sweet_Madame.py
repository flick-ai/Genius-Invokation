from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Sweet_Madame(FoodCard):
    id: int = 33300521
    name: str = "Sweet Madame"
    name_ch = "甜甜花酿鸡"
    cost_num = 0
    cost_type = None

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = None

    def on_played(self, game: 'GeniusGame'):
        target_character = super().on_played(game)
        target_character.heal(heal=1,game=game)
    
    def find_target(self, game: 'GeniusGame'):
        target_list = []
        for idx, character in enumerate(game.active_player.character_list):
            if not character.is_satisfy and character.health_point != character.max_health_point:
                target_list.append(idx+2)
        return target_list
        

    