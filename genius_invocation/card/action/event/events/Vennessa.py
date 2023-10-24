from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Vennessa(ActionCard):
    id: int = 332019
    name: str = 'The Legend of Vennessa'
    name_ch = "温妮莎传奇"
    cost_num = 3
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        dices = game.active_player.roll_dice(num=4, is_basic=True, is_different=True)
        game.active_player.dice_zone.add(dices)
