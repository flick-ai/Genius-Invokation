from card.character.base import Damage
from collections import defaultdict
from typing import List, TYPE_CHECKING
from utils import *

if TYPE_CHECKING:
    from game.game import GeniusGame

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
        # self.name: str = name
        # self.event_types = [
        #     'equipment', 
        #     'artifact',
        #     'support',
        #     'summon',
        #     'active',
        #     'character',
        # ]
        self.listeners: dict(ListenerList) = {}
        for zone_type in ZoneType:
            self.listeners[zone_type] = ListenerList([])


class ListenerList(object):
    def __init__(self, actions) -> None:
        self.head = ListenerNode(None)
        self.tail = self.head
        for action in actions:
            self.append_action(action)
    
    def append_action(self, action) -> ListenerNode:
        self.tail.next = ListenerNode(action, self.tail)
        self.tail = self.tail.next
        return self.tail
    
    def append(self, listener: ListenerNode) -> ListenerNode:
        self.tail.next = listener
        self.tail = self.tail.next
        return self.tail

    def __call__(self, game: 'GeniusGame') -> None:
        listener = self.head.next
        while listener:
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
        return self.events[event_type][zone_type].append_action(action)

    def invoke(self, event_type, game: 'GeniusGame') -> None:
        for zone_type in ZoneType:
            self.events[event_type][zone_type](game)




# class OnDealDamageEvent(ListenerNode):


# class Event:
#     '''事件基类'''
#     def __init__(self) -> None:
#         pass

#     def add_to_event_list(self, game: GeniusGame) -> None:
#         pass

#     def remove_from_event_list(self, game: GeniusGame) -> None:
#         pass
    
#     def on_call(self, game: GeniusGame) -> None:
#         pass

# class OnDealDamageEvent(Event):
#     def __init__(self):
#         pass

#     def on_call(self, game: GeniusGame, damage: Damage) -> None:
#         pass