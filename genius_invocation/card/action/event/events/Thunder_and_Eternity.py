from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Thunder_and_Eternity(ActionCard):
    id: int = 331803
    name: str = 'Thunder and Eternity'
    name_ch = '雷与永恒'
    time = 3.7
    country = CountryType.INAZUMA
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT_COUNTRY

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        num = game.active_player.dice_zone.num()
        game.active_player.dice_zone.remove_all()
        game.active_player.dice_zone.add([DiceType.OMNI.value for i in range(num)])

    def find_target(self, game:'GeniusGame'):
        if game.active_player.dice_zone.num()>0:
            return [1]
        else:
            return []
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.0] = "调整了事件牌「雷与永恒」的效果：现在该事件牌可以将我方所有元素骰转换为万能元素"
        return log
