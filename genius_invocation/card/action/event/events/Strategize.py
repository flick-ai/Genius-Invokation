from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Strategize(ActionCard):
    id: int = 332004
    name: str = 'Strategize'
    name_ch = '运筹帷幄'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        self.now_phase: GamePhase

    def on_played(self, game: 'GeniusGame'):
        self.now_phase = game.game_phase
        game.game_phase = GamePhase.SET_CARD
        game.special_phase = self
        game.active_player.get_card(num=2)
