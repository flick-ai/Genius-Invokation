from typing import TYPE_CHECKING
from utils import *
if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import EventNode


class Entity:
    def __init__(self):
        self.entity_type: ZoneType
        self.events: dict[str, EventNode] = {}
        self.registered_events: list(EventNode) = []

    def register_all_events(self, game: GeniusGame):
        for event in self.events:
            self.registered_events.append(game.manager.register(event, self.events[event]))
        game.manager.register('before_skill', 'on_damage', 'after_skill')

    def on_distroy(self):
        for event in self.registered_events:
            event.del_node()
