from ...base import ActionCard
from utils import *
if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer

class Nature_and_Wisdom(ActionCard):
    id: int = 5320033 # TODO: 还不知道,随手写的
    name: str = 'Nature and Wisdom'
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
        game.active_player.get_card(num=1)

    def on_finished(self, game: 'GeniusGame'):
        game.game_phase = self.now_phase
        game.special_phase = None