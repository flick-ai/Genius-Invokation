from genius_invocation.card.character.base import Damage
from collections import defaultdict
from typing import Any, List, TYPE_CHECKING, Dict
from genius_invocation.utils import *
from loguru import logger
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class ListenerNode:
    '''监听者节点'''
    def __init__(self, action, before=None, next=None):
        self.action = action
        self.before = before
        self.next = next

    def remove(self):
        if self.before:
            self.before.next = self.next
        if self.next:
            self.next.before = self.before

    def __call__(self, game: 'GeniusGame') -> None:
        self.action(game)


class Event:
    def __init__(self) -> None:
        self.listeners: Dict[ZoneType, ListenerCircles] = {}
        for zone_type in ZoneType:
            if zone_type == ZoneType.CHARACTER_ZONE:
                self.listeners[zone_type] = ListenerCircles(need_character=True)
            else:
                self.listeners[zone_type] = ListenerCircles()

    def __call__(self, zone_type):
        return self.listeners[zone_type]

class ListenerCircle(object):
    def __init__(self, need_character=False) -> None:
        self.need_character = need_character
        self.head = ListenerNode(None)
        self.head.next = self.head
        self.head.before = self.head
        self.tail = self.head
        if self.need_character:
            self.character_heads = [ListenerNode(None) for _ in range(3)]
            self.character_tails = [self.character_heads[(i + 1) % 3] for i in range(3)]
            for i in range(3):
                self.character_heads[i].next = self.character_heads[(i + 1) % 3]
                self.character_heads[i].before = self.character_heads[(i - 1) % 3]


    def append_action(self, action, character_index=None) -> ListenerNode:
        if character_index:
            node = ListenerNode(action, self.character_tails[character_index].before, self.character_tails[character_index])
            self.character_tails[character_index].before.next = node
            self.character_tails[character_index].before = node
            return node
        else:
            node = ListenerNode(action, self.tail.before, self.tail)
            self.tail.before.next = node
            self.tail.before = node
            return node

    def __call__(self, game: 'GeniusGame', character_index=None) -> None:
        if not character_index:
            listener = self.head.next
            tail_before = self.tail.before
            while listener != self.tail:
                listener(game)
                if listener == tail_before: break
                listener = listener.next
        else:
            listener = self.character_heads[character_index].next
            tail_before = self.character_heads[character_index].before
            while listener != self.character_heads[character_index]:
                if listener in self.character_heads:
                    listener = listener.next
                    continue
                listener(game)
                if listener == tail_before: break
                listener = listener.next



class ListenerCircles(object):
    def __init__(self, need_character=False) -> None:
        self.needs_character = need_character
        self.player_lisnters = [ListenerCircle(need_character=need_character) for _ in range(2)]

    def append_action(self, action, player_index, character_index) -> ListenerNode:
        return self.player_lisnters[player_index].append_action(action, character_index)

    def __call__(self, game: 'GeniusGame') -> None:
        player_index = game.active_player_index
        player0_character_index = get_active_character(game, 0).index if self.needs_character else None
        player1_character_index = get_active_character(game, 1).index if self.needs_character else None

        self.player_lisnters[player_index](game, player0_character_index)
        self.player_lisnters[1 - player_index](game, player1_character_index)




'''
事件种类
'''

class EventManager:
    def __init__(self) -> None:
        self.events = defaultdict(Event)

    def listen(self, event_type: EventType, zone_type: ZoneType, action, player_index, characetr_index) -> ListenerNode:
        '''
        监听事件
        event_type: 事件类型
        zone_type: zone类型
        action: 监听动作
        '''
        return self.events[event_type](zone_type).append_action(action, player_index, characetr_index)

    def invoke(self, event_type, game: 'GeniusGame') -> None:
        for zone_type in ZoneType:
            self.events[event_type](zone_type)(game)
