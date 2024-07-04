from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Master_Zhang_Entity(Support):
    id: int = 322018
    name = 'Master Zhang'
    name_ch = '老章'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage= self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage > 0:
                if game.current_dice.use_type == ActionCardType.EQUIPMENT_WEAPON:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        weapon_num = 0
                        for character in self.from_player.character_list:
                            if character.character_zone.weapon_card != None:
                                weapon_num += 1
                        game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-1-weapon_num)
                        return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
        ]
    def show(self):
        if self.usage>0:
            return '^v^'
        else:
            return '-_-'


class Master_Zhang(SupportCard):
    '''
        老章
    '''
    id: int = 322018
    name: str = 'Master Zhang'
    name_ch = '老章'
    time = 3.8
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Master_Zhang_Entity(game, from_player=game.active_player)
        super().on_played(game)
