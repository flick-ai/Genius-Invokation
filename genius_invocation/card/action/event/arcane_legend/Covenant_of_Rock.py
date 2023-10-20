from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Covenant_of_Rock(ActionCard):
    id: int = 330002
    name: name = "Covenant of Rock"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        dices = game.active_player.roll_dice(num=2, is_basic=True, is_different=True)
        game.active_player.dice_zone.add(dices)
    
    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        if game.active_player.dice_zone.num() == 0:
            return [1]
        else:
            return []
