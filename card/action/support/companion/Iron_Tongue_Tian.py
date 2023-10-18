from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Iron_Tongue_Tian_Entity(Support):
    id: int = 322011
    name = 'Iron_Tongue_Tian'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            character = get_my_active_character(game)
            if character.power != character.max_power:
               character.power += 1
               self.usage -= 1
            else:
                for character in get_my_standby_character(game):
                    if character.power != character.max_power:
                        character.power += 1
                        self.usage -= 1
                        break
            if self.usage == 0:
                self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]


class Iron_Tongue_Tian(SupportCard):
    '''
        田铁嘴
    '''
    id: int = 322011
    name: str = 'Iron Tongue Tian'
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Iron_Tongue_Tian_Entity(game, from_player=game.active_player)
        super().on_played(game)
