from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Best_Companion(ActionCard):
    id: int = 332001
    name: str = 'The Bestest Travel Companion!'
    name_ch = '最好的伙伴！'
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        game.active_player.dice_zone.add([DiceType.OMNI.value, DiceType.OMNI.value])
