from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Liben_Entity(Support):
    id: int = 322008
    name = 'Liben'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.dice = []

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            dices = self.from_player.dice_zone.show()
            omni_num = dice.count(7)
            put_into = []
            #
            for idx, dice in enumerate(dices):
                if dice not in put_into:
                    self.from_player.dice_zone.remove([idx])
                    put_into.append(dice)
                    if len(put_into) + len(self.dice) == self.max_count:
                        self.dice = self.dice + put_into
                        return
            for i in range(omni_num-1):
                put_into.append(7)
                if len(put_into) + len(self.dice) == self.max_count:
                    self.dice = self.dice + put_into
                    return
            self.dice = self.dice + put_into

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if len(self.dice) == 3:
                self.from_player.get_card(num=2)
                self.from_player.dice_zone.add([DiceType.OMNI.value, DiceType.OMNI.value])
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end)
        ]


class Liben(SupportCard):
    '''
        立本
    '''
    id: int = 322008
    name: str = 'Liben'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Liben_Entity(game, from_player=game.active_player)
        super().on_played(game)
