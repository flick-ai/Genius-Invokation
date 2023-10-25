from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Friendship_Eternal(ActionCard):
    id: int = 332020
    name: str = 'Friendship Eternal'
    name_ch = "永远的友谊"
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        my_num = game.active_player.hand_zone.num()
        if my_num < 4:
            game.active_player.get_card(num=4-my_num)

        opponent_num = get_opponent(game).hand_zone.num()
        if opponent_num < 4:
            get_opponent(game).get_card(num=4-opponent_num)
