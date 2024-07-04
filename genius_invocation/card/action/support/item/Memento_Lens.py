from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Memento_Lens_Entity(Support):
    id: int = 323006
    name: str = 'Memento Lens'
    name_ch = '留念镜'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage_round = -1
        self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.active_player_index == self.from_player.index:
                if game.current_dice.use_type in [ActionCardType.EQUIPMENT_WEAPON,
                                                  ActionCardType.EQUIPMENT_ARTIFACT,
                                                  ActionCardType.SUPPORT_LOCATION,
                                                  ActionCardType.SUPPORT_COMPANION,]:
                    if game.current_dice.name in self.from_player.played_cards:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-2)
                            return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage_round = game.round
            self.usage -= 1
            if self.usage == 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
        ]
        

class Memento_Lens(SupportCard):
    id: int = 323006
    name: str = 'Memento Lens'
    name_ch = '留念镜'
    time = 4.3
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Memento_Lens_Entity(game, from_player=game.active_player)
        super().on_played(game)
