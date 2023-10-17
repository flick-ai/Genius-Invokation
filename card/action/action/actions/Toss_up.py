from ...base import ActionCard
from utils import *
if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer

class Toss_up(ActionCard):
    id: int = 332003
    name: str = 'Toss-up'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        now_phase = game.game_phase
        game.game_phase = GamePhase.ROLL_PHASE
        game.is_special_phase = True
        
