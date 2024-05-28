from genius_invocation.card.action.base import ActionCard
from genius_invocation.entity.status import Status
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class Controlled_Directional_Blast(ActionCard):
    id: int = 332030
    name: str = 'Controlled Directional Blast'
    name_ch = '可控性去危害化式定向爆破'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        for player in game.players:
            for summon in player.summon_zone.space:
                summon.minus_usage(game, 1)

    def find_target(self, game: 'GeniusGame'):
        if get_opponent(game).support_zone.num() + get_opponent(game).summon_zone.num() >=4:
            return [1]
        else:
            return []
