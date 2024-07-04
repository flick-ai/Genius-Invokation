from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Undersea_Treasure(ActionCard):
    name: str = 'Underwater Treasure'
    name_ch = '海底宝藏'
    cost_num = 0
    cost_type = None
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        get_my_active_character(game).heal(1, game)
        dices = game.active_player.roll_dice(num=1, is_basic=True)
        game.active_player.dice_zone.add(dices)


class Underwater_Treasure_Hunt(ActionCard):
    id: int = 332031
    name: str = 'Underwater Treasure Hunt'
    name_ch = '海中寻宝'
    time = 4.6
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        self.num = 6

    def on_played(self, game: 'GeniusGame'):
        cards = [Undersea_Treasure() for _ in range(6)]
        game.active_player.card_zone.insert_randomly(cards, num=-1)
