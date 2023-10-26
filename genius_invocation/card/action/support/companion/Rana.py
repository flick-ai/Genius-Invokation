from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Rana_Entity(Support):
    id: int = 322017
    name = 'Rana'
    name_ch = '拉娜'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_skill(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage > 0:
                if game.current_skill.type == SkillType.ELEMENTAL_SKILL:
                    standby_character = get_my_standby_character(game)
                    if standby_character == []:
                        return
                    else:
                        next_character = standby_character[0]
                        dice_type = ElementToDice[next_character.element]
                        self.from_player.dice_zone.add([dice_type.value])
                        self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
        ]
    def show(self):
        if self.usage > 0:
            return "^v^"
        else:
            return "-_-"

class Rana(SupportCard):
    '''
        拉娜
    '''
    id: int = 322017
    name: str = 'Rana'
    name_ch = '拉娜'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Rana_Entity(game, from_player=game.active_player)
        super().on_played(game)
