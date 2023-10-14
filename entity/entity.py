from typing import TYPE_CHECKING, List, Tuple
from utils import *
if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode
    from game.player import GeniusPlayer
    from entity.character import Character

class Entity:
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None):
        self.entity_type: ZoneType
        self.listeners: List(Tuple(EventType, ZoneType, function)) = [] # list of (event_type, event_zone, action) tuples
        self.registered_events: list(ListenerNode) = []
        self.from_player = from_player
        self.from_character = from_character
        self.update_listener_list()
        self.listen_all(game)

    def update_listener_list(self):
        pass

    def listen_all(self, game: 'GeniusGame'):
        for event_name, event_type, action in self.listeners:
            self.registered_events.append(game.manager.listen(event_name, event_type, action))

    def on_destroy(self, game):
        for action in self.registered_events:
            action.remove()
