from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class CountdowntotheShow3(ActionCard):
    id: int = 332032
    base_name: str = 'Countdown to the Show: '
    name: str = 'Countdown to the Show: 3'
    name_ch = "幻戏倒计时: 3"
    cost_num = 3
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        num = game.active_player.dice_zone.num()
        game.active_player.dice_zone.remove_all()
        game.active_player.dice_zone.add([DiceType.OMNI.value for i in range(num)])
        game.active_player.get_card(num=4)

    def find_target(self, game:'GeniusGame'):
        if game.active_player.dice_zone.num() > self.cost_num:
            return [1]
        else:
            return []

    def on_discard(self, game: 'GeniusGame'):
        target_card_name = self.base_name + str(self.cost_num - 1)
        target_card = eval(target_card_name)()
        game.active_player.card_zone.insert_randomly(target_card, num=0)

class CountdowntotheShow2(CountdowntotheShow3):
    name: str = 'Countdown to the Show: 2'
    name_ch = "幻戏倒计时: 2"
    cost_num = 2

class CountdowntotheShow1(CountdowntotheShow3):
    name: str = 'Countdown to the Show: 1'
    name_ch = "幻戏倒计时: 1"
    cost_num = 1

class CountdowntotheShow0(CountdowntotheShow3):
    name: str = 'Countdown to the Show: 0'
    name_ch = "幻戏倒计时: 0"
    cost_num = 0


