from game.game import GeniusGame
from utils import *
from entity.entity import Entity
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode
    from game.player import GeniusPlayer

class Support(Entity):
    # 支援基本类
    id: int
    name: str
    element: ElementType
    remain_use: int
    usage: int
    max_usage: int
    skills: list

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage: int = self.usage

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_player.support_zone.destroy(self)