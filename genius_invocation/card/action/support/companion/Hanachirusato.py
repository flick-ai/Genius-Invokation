from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Hanachirusato_Entity(Support):
    id: int = 322013
    name = 'Hanachirusato'
    name_ch = '花散里'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.cleansing_ritual_progress = 0

    def on_remove(self, game:'GeniusGame'):
        if self.cleansing_ritual_progress < self.max_count:
            self.cleansing_ritual_progress += 1

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_WEAPON or game.current_dice.use_type == ActionCardType.EQUIPMENT_ARTIFACT:
                if self.cleansing_ritual_progress == self.max_count:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-2)
                        return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.ON_SUMMON_REMOVE, ZoneType.SUPPORT_ZONE, self.on_remove)
        ]
    def show(self):
        return str(self.cleansing_ritual_progress)


class Hanachirusato(SupportCard):
    '''
        花散里
    '''
    id: int = 322013
    name: str = 'Hanachirusato'
    name_ch = '花散里'
    time = 3.7
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Hanachirusato_Entity(game, from_player=game.active_player)
        super().on_played(game)
