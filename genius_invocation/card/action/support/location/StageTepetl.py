from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class StageTepetlEntity(Support):
    name = 'Stage Tepetl'
    name_ch = '特佩利舞台'
    id = 32102361
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.attention = 0

    def after_use_skill(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.attention += 1
        else:
            self.attention -= 1

    def after_use_special(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.attention += 1
        else:
            self.attention -= 1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.attention >= 1:
                num = self.from_player.dice_zone.num()
                self.from_player.dice_zone.remove([num-1])
                self.from_player.dice_zone.add([DiceType.OMNI for _ in range(1)])
            if self.attention >= 3:
                dice = self.from_player.roll_dice(num=1, is_basic=True)
                self.from_player.dice_zone.add(dice)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.after_use_skill),
            (EventType.AFTER_USE_SPECIAL, ZoneType.SUPPORT_ZONE, self.after_use_special),
        ]

    def show(self):
        return str(self.attention)

class StageTepetl(SupportCard):
    id: int = 321023
    name = 'Stage Tepetl'
    name_ch = '特佩利舞台'
    time = 5.1
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = StageTepetlEntity(game, from_player=game.active_player)
        super().on_played(game)