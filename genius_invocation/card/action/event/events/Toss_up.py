from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Toss_up(ActionCard):
    id: int = 332003
    name: str = 'Toss-up'
    name_ch = '一掷乾坤'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()
        self.now_phase: GamePhase

    def on_played(self, game: 'GeniusGame'):
        self.now_phase = game.game_phase
        game.game_phase = GamePhase.ROLL_PHASE
        game.active_player.roll_time = 2
        game.special_phase = self

    def on_finished(self, game: 'GeniusGame'):
        game.game_phase = self.now_phase
        game.special_phase = None
        game.resolve_action(None)

    def find_target(self, game:'GeniusGame'):
        if game.active_player.dice_zone.num()>0:
            return [1]
        else:
            return []

