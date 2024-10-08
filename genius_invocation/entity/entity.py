from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.entity.character import Character

class Entity:
    name: str
    name_ch: str = ""
    id: int
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None):
        self.entity_type: ZoneType
        self.listeners: List[Tuple(EventType, ZoneType, function)] = [] # list of (event_type, event_zone, action) tuples
        self.registered_events: List[ListenerNode] = []
        self.from_player = from_player
        self.from_character = from_character
        self.update_listener_list()
        self.listen_all(game)

    def update_listener_list(self):
        pass

    def listen_all(self, game: 'GeniusGame'):
        player_index = self.from_player.index
        from genius_invocation.entity.character import Character
        if isinstance(self, Character):
            character_index = self.index
        else:
            character_index = self.from_character.index if self.from_character is not None else None
        for event_name, event_type, action in self.listeners:
            self.registered_events.append(game.manager.listen(event_name, event_type, action, player_index, character_index))

    def listen_event(self, game:'GeniusGame', event_name: EventType, event_type: ZoneType, action: 'Action'):
        player_index = self.from_player.index
        from genius_invocation.entity.character import Character
        if isinstance(self, Character):
            character_index = self.index
        else:
            character_index = self.from_character.index if self.from_character is not None else None
        self.registered_events.append(game.manager.listen(event_name, event_type, action, player_index, character_index))

    def on_destroy(self, game):
        for action in self.registered_events:
            action.remove()

    def update(self):
        pass

    def show(self):
        return self.name