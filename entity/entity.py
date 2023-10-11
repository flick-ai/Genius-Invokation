from typing import TYPE_CHECKING, List, Tuple
from utils import *
if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode


class Entity:
    def __init__(self, game: GeniusGame):
        self.entity_type: ZoneType
        self.listeners: List(Tuple(str, str, function)) = [] # list of (event_name, event_type, action) tuples
        self.registered_events: list(ListenerNode) = []
        self.update_listener_list(game)
        self.listen_all(game)

    def update_listener_list(self, game: GeniusGame):
        pass

    def listen_all(self, game: GeniusGame):
        for event_name, event_type, action in self.listeners:
            self.registered_events.append(game.manager.listen(event_name, event_type, action))

    def on_distroy(self):
        for action in self.registered_events:
            action.remove()
