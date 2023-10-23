from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Send_Off(ActionCard):
    id: int = 332013
    name: str = 'Send Off'
    name_ch = '送你一程'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        get_opponent(game).summon_zone.space[game.current_action.target_idx].minus_usage(game ,2)

    def find_target(self, game: 'GeniusGame'):
        target = []
        for i in range(get_opponent(game).summon_zone.num()):
            target.append(i+5)
