from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Starsigns(ActionCard):
    id: int = 332008
    name: str = 'Starsigns'
    name_ch = '星天之兆'
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        get_my_active_character(game).power += 1

    def find_target(self, game: 'GeniusGame'):
        character = get_my_active_character(game)
        if character.power != character.max_power:
            return [game.active_player.active_idx]
        return []