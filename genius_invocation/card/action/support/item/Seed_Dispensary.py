from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Seed_Dispensary_Entity(Support):
    id: int = 323005
    name = 'Seed Dispensary'
    name_ch = '化种匣'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage_round = -1

    def on_calculate(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.active_player_index == self.from_player.index:
                if game.current_dice.use_type in [ActionCardType.SUPPORT_ITEM,
                                                ActionCardType.SUPPORT_LOCATION,
                                                ActionCardType.SUPPORT_COMPANION,]:
                    if game.current_dice.origin_cost[0]['cost_num'] > 2:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-1)
                        return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage_round = game.round

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
        ]
    def show(self):
        return str(self.treasure_clues)

class Seed_Dispensary(SupportCard):
    id: int = 323005
    name: str = 'Seed Dispensary'
    name_ch = '化种匣'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Seed_Dispensary_Entity(game, from_player=game.active_player)
        super().on_played(game)
