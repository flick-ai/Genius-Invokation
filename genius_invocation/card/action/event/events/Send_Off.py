from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Send_Off(ActionCard):
    id: int = 332013
    name: str = 'Send Off'
    name_ch = '送你一程'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        get_opponent(game).summon_zone.space[game.current_action.target_idx].minus_usage(game ,2)

    def find_target(self, game: 'GeniusGame'):
        target = []
        for i in range(get_opponent(game).summon_zone.num()):
            target.append(i+5)
        return target

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.7] = ["调整了「七圣召唤」中，事件牌「送你一程」的效果：由“选择一个敌方「召唤物」，将其消灭”改为“选择一个敌方「召唤物」，使其「可用次数」-2”",
                    "调整了「七圣召唤」中，事件牌「送你一程」的所需元素骰费用：所需元素骰费用由2个任意元素骰调整为2个相同元素骰；"]
        return log
