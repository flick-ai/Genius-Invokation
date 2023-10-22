from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Thunder_and_Eternity(ActionCard):
    id: int = 331803
    name: str = 'Thunder and Eternity'
    name_ch = '雷与永恒'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        num = game.active_player.dice_zone.num()
        game.active_player.dice_zone.remove_all()
        game.active_player.dice_zone.add([7 for i in range(num)])