from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Chef_Mao_Entity(Support):
    id: int = 322005
    name = 'Chef Mao'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage_round = self.max_usage
        self.usage_game = self.max_usage

    def on_after(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EVENT_FOOD:
                if self.usage_round > 0:
                    self.from_player.dice_zone.add(self.from_player.roll_dice(num=1, is_basic=True))
                if self.usage_game > 0:
                    card = self.from_player.card_zone.find_card(card_type=ActionCardType.EVENT_FOOD)
                    self.from_player.hand_zone.add([card])

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage_round = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin)
        ]

class Chef_Mao(SupportCard):
    '''
        卯师傅
    '''
    id: int = 322005
    name: str = 'Chef Mao'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Chef_Mao_Entity(game, from_player=game.active_player)
        super().on_played(game)
