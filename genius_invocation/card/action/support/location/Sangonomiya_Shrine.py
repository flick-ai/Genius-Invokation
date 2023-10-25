from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Sangonomiya_Shrine_Entity(Support):
    id: int = 321009
    name = 'Sangonomiya Shrine'
    name_ch = '珊瑚宫'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            need_heal = False
            for character in self.from_player.character_list:
                if character.is_alive and character.health_point != character.max_health_point:
                    need_heal = True
                    break
            if need_heal:
                for character in self.from_player.character_list:
                    character.heal(heal=1,game=game)
                self.usage -= 1
                if self.usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]
    def show(self):
        return str(self.usage)

class Sangonomiya_Shrine(SupportCard):
    '''
        珊瑚宫
    '''
    id: int = 321009
    name: str = 'Sangonomiya Shrine'
    name_ch = '珊瑚宫'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Sangonomiya_Shrine_Entity(game, from_player=game.active_player)
        super().on_played(game)