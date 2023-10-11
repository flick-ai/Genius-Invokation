from card.character.base import Damage
from game.game import GeniusGame
from collections import defaultdict
from typing import List




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

    def __call__(self, game: GeniusGame) -> None:
        self.action(game)


class Event:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.event_types = [
            'equipment', 
            'artifact',
            'support',
            'summon',
            'active',
            'character',
        ]
        self.listeners: dict(ListenerList) = {}
        for event_type in self.event_types:
            self.listeners[event_type] = ListenerList([])


class ListenerList(object):
    def __init__(self, actions: List(function)) -> None:
        self.head = ListenerNode(None)
        self.tail = self.head
        for action in actions:
            self.append_action(action)
    
    def append_action(self, action: function) -> ListenerNode:
        self.tail.next = ListenerNode(action, self.tail)
        self.tail = self.tail.next
        return self.tail
    
    def append(self, listener: ListenerNode) -> ListenerNode:
        self.tail.next = listener
        self.tail = self.tail.next
        return self.tail

    def __call__(self, game: GeniusGame) -> None:
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
    
    def listen(self, event_name: str, event_type: str, action: function) -> ListenerNode:
        '''
        监听事件
        event_name: 事件名称
        event_type: 事件类型, 即zone类型
        action: 监听动作
        '''
        return self.events[event_name][event_type].append_action(action)
    
    def invoke(self, event_name, game: GeniusGame) -> None:
        for event_type in self.events[event_name].event_types:
            self.events[event_name].listeners[event_type](game)





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