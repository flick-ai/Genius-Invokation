from genius_invocation.card.character.base import Damage
from collections import defaultdict
from typing import Any, List, TYPE_CHECKING
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
        self.listeners: dict(ListenerList) = {}
        for zone_type in ZoneType:
            self.listeners[zone_type] = ListenerList([])

    def __call__(self, zone_type):
        return self.listeners[zone_type]


class ListenerList(object):
    def __init__(self, actions) -> None:
        self.head = ListenerNode(None)
        self.tail = ListenerNode(None)
        self.head.next = self.tail
        self.tail.before = self.head
        for action in actions:
            self.append_action(action)

    def append_action(self, action) -> ListenerNode:
        node = ListenerNode(action, self.tail.before, self.tail)
        self.tail.before.next = node
        self.tail.before = node
        return node

    def append(self, listener: ListenerNode) -> ListenerNode:
        listener.before = self.tail.before
        listener.next = self.tail
        self.tail.before.next = listener
        self.tail.before = listener
        return listener

    def __call__(self, game: 'GeniusGame') -> None:
        listener = self.head.next
        while listener!=self.tail:
            listener(game)
            listener = listener.next


'''
事件种类
'''

class EventManager:
    def __init__(self) -> None:
        self.events = defaultdict(Event)

    def listen(self, event_type: EventType, zone_type: ZoneType, action) -> ListenerNode:
        '''
        监听事件
        event_type: 事件类型
        zone_type: zone类型
        action: 监听动作
        '''
        return self.events[event_type](zone_type).append_action(action)

    def invoke(self, event_type, game: 'GeniusGame') -> None:
        for zone_type in ZoneType:
            self.events[event_type](zone_type)(game)
