from genius_invocation.card.action.base import ActionCard
from genius_invocation.utils import *
from genius_invocation.entity.status import Status
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class InEveryHouseaStove(ActionCard):
    id: int = 330005
    name = "In Every House a Stove"
    name_ch = "万家灶火"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT_ARCANE_LEGEND
    def __init__(self) -> None:
        super().__init__()

    def check__different_talent(self, card_names, card_types):
        # 4.7平衡性调整：第一回合使用时抽取天赋
        # 检查至少存在两个不同的天赋
        talent_name = []
        for idx, card_type in enumerate(card_types):
            if card_type == ActionCardType.EQUIPMENT_TALENT:
                if card_names[idx] not in talent_name:
                    talent_name.append(card_names[idx])
        if len(talent_name) >= 2:
            return True
        return False
        
    def on_played(self, game: 'GeniusGame') -> None:
        # 更新,回合-1
        # 4.7平衡性调整：第一回合使用时抽取天赋
        if game.round == 1:
            cards = game.active_player.card_zone.random_find_card(card_type=ActionCardType.EQUIPMENT_TALENT, num=1)
            game.active_player.hand_zone.add(cards)
        else:
            game.active_player.get_card(num=min(4, game.round - 1))


    def find_target(self, game: 'GeniusGame'):
        if game.active_player.play_arcane_legend:
            return []
        else:
            # 4.7平衡性调整：第一回合使用时抽取天赋
            if game.round == 1:
                if self.check__different_talent(game.active_player.card_zone.get_card_names(), 
                                            game.active_player.card_zone.get_card_types()):
                    return [1]
                else: 
                    return []
            return [1]
