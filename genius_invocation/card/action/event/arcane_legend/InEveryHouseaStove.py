from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class InEveryHouseaStove(ActionCard):
    id: int = 330005
    name: name = "In Every House a Stove"
    name_ch = "万家灶火"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.get_card(num=min(4, game.round))

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        else:
            return [1]
