from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Treasure_Seeking_Seelie_Entity(Support):
    id: int = 323004
    name = 'Treasure-Seeking Seelie'
    name_ch = '寻宝仙灵'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.treasure_clues = 0

    def on_after(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.treasure_clues += 1
            if self.treasure_clues == self.max_count:
                self.from_player.get_card(num=3)
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_after),
        ]
    def show(self):
        return str(self.treasure_clues)

class Treasure_Seeking_Seelie(SupportCard):
    '''
        寻宝仙灵
    '''
    id: int = 323004
    name: str = 'Treasure-Seeking Seelie'
    name_ch = '寻宝仙灵'
    time = 3.7
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Treasure_Seeking_Seelie_Entity(game, from_player=game.active_player)
        super().on_played(game)
