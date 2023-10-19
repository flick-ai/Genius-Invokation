from genius_invocation.utils import *
from genius_invocation.entity.entity import Entity
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer

class Support(Entity):
    # 支援基本类
    id: int
    name: str
    max_usage: int
    max_count: int

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_player.support_zone.destroy(self)