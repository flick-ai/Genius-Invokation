from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class ViciousAncientBattle(ActionCard):
    id: int = 330008
    name = "Vicious Ancient Battle"
    name_ch = "旧日鏖战"
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        get_opponent_active_character(game).loose_power(power=1)

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        if get_opponent_active_character(game).power > 0:
            return [1]
        else:
            return []
