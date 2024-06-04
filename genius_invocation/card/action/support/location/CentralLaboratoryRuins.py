from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class CentralLaboratoryRuinsEntity(Support):
    name = 'Central Laboratory Ruins'
    name_ch = '中央实验室遗址'
    max_usage = 9
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.experimentalprogress = 0

    def excute(self, game):
        if self.experimentalprogress > 0:
            if self.experimentalprogress % 3 == 0:
                self.from_player.dice_zone.add([DiceType.OMNI.value])
            if self.experimentalprogress == self.max_usage:
                self.on_destroy(game)

    def on_tune_card(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.experimentalprogress += 1
            self.excute(game)

    def on_discard_card(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.experimentalprogress += 1
            self.excute(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_TUNE_CARD, ZoneType.SUPPORT_ZONE, self.on_tune_card),
            (EventType.ON_DISCARD_CARD, ZoneType.SUPPORT_ZONE, self.on_discard_card),
        ]
    def show(self):
        return str(self.usage)

class CentralLaboratoryRuins(SupportCard):
    id: int = 321017
    name = 'Central Laboratory Ruins'
    name_ch = '中央实验室遗址'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = CentralLaboratoryRuinsEntity(game, from_player=game.active_player)
        super().on_played(game)