from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Quick_Knit(ActionCard):
    id: int = 332012
    name: str = 'Quick Knit'
    name_ch = '快快缝补术'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        target_idx = game.current_action.target_idx
        game.active_player.summon_zone.space[target_idx].add_usage(game, count=1)
    
    def find_target(self, game: 'GeniusGame'):
        target = []
        for i in range(game.active_player.summon_zone.num()):
            target.append(i+5)
