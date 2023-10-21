from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Mushroom_Pizza_Entity(Status):
    id: int = 333007
    name: str = "Mushroom Pizza"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.from_character.heal(heal=1)
        self.current_usage = 2
    
    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_character.heal(int=1)
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end),
        ]

class Mushroom_Pizza(FoodCard):
    id: int = 333007
    name: str = "Mushroom Pizza"
    cost_num = 1
    cost_type = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)
        

    