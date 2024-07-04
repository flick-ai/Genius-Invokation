from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Lumenstone_Adjuvant_Entity(Support):
    id: int = 323007
    name: str = 'Lumenstone Adjuvant'
    name_ch = '流明石触媒'
    max_usage = 3
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage_round = -1
        self.count = 0
        self.usage = self.max_usage

    def on_play(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.active_player_index == self.from_player.index:
                if game.current_card.card_type in ActionCardType:
                    self.count += 1
                    if self.count == self.max_count:
                        self.usage_round = game.round
                        self.from_player.get_card(num=1)
                        self.from_player.dice_zone.add([DiceType.OMNI.value])
                        self.usage -= 1
                        if self.usage == 0:
                            self.on_destroy(game)

    def on_end(self, game:'GeniusGame'):
        self.count = 0


    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.FINAL_END, ZoneType.SUPPORT_ZONE, self.on_end),
        ]
    def show(self):
        return str(self.usage)

class Lumenstone_Adjuvant(SupportCard):
    id: int = 323007
    name: str = 'Lumenstone Adjuvant'
    name_ch = '流明石触媒'
    time = 4.5
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Lumenstone_Adjuvant_Entity(game, from_player=game.active_player)
        super().on_played(game)
