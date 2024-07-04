from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Joyous_Celebration(ActionCard):
    id: int = 330003
    name = "Joyous Celebration"
    name_ch = "愉舞欢游"
    time = 4.0
    cost_num = 0
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        element = get_my_active_character(game).element
        for character in game.active_player.character_list:
            # 4.2更新
            if len(character.elemental_application)>0:
                character.elemental_attach(game, element)

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        element = get_my_active_character(game).element
        if element != ElementType.ANEMO and element != ElementType.GEO:
            return [1]
        else:
            return []
        
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.3] = "调整了事件牌「愉舞欢游」所需元素骰：所需元素骰由1个元素骰调整为0个"
        return log