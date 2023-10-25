from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Guardians_Oath(ActionCard):
    id: int = 332014
    name: str = "Guardian's Oath"
    name_ch = '护法之誓'
    cost_num = 4
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        for i in range(game.active_player.summon_zone.num()):
            game.active_player.summon_zone.destroy(i)
        for i in range(get_opponent(game).summon_zone.num()):
            get_opponent(game).summon_zone.destroy(i)
    
    def find_target(self, game: 'GeniusGame'):
        if game.active_player.summon_zone.num()+get_opponent(game).summon_zone.num() > 0:
            return [1]
        else:
            return []
