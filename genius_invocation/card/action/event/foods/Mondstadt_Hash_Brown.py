from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.card.action.event.base import FoodCard
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Mondstadt_Hash_Brown(FoodCard):
    id: int = 333006
    name: str = "Mondstadt Hash Brown"
    cost_num = 1
    cost_type = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.food_entity = None

    def on_played(self, game: 'GeniusGame'):
        target_character = super().on_played(game)
        target_character.heal(int=2)
        

    