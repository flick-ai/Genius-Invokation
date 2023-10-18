from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Vanarana_Entity(Support):
    id: int = 321011
    name = 'Vanarana'
    max_usage = -1
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.dice = []

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            dices = self.from_player.dice_zone.show()
            if dices == None:
                return
            else:
                sort_map = self.sort_dice(self.from_player.dice_zone.space)
                sorted_dices = sorted(dices, key=lambda x:sort_map[x], reverse=True)
            for dice in dices:
                self.dice.append(dice)
                if len(self.dice) == self.max_count:
                    return

    def sort_dice(self, dices):
        sort_map = {i:DICENUM-i for i in range(DICENUM)}
        sum_dice = dices.sum(axis=0)[:-1]
        for i in range(DICENUM-1):
            sort_map[i] += 10 * sum_dice[i]
        sort_map[7] = 0
        return sort_map

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            self.from_player.dice_zone.add(self.dice)
            self.dice = []

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]


class Vanarana(SupportCard):
    '''
        桓那兰那
    '''
    id: int = 321011
    name: str = 'Vanarana'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Vanarana_Entity(game, from_player=game.active_player)
        super().on_played(game)