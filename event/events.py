from card.character.base import Damage
from game.game import GeniusGame
from collections import defaultdict




class EventNode:
    '''事件节点'''
    def __init__(self, action, before=None, next=None):
        self.event = action
        self.before = before
        self.next = next
    
    def del_node(self):
        if self.before:
            self.before.next = self.next
        if self.next:
            self.next.before = self.before

    def on_call(self, game: GeniusGame) -> None:
        self.event(game)


class EventListDict:
    def __init__(self) -> None:
        self.event_lists: dict(EventList) = {
            'equipment': EventList([]),
            'artifact': EventList([]),
            'support': EventList([]),
            'summon': EventList([]),
            'active': EventList([]),
            'character': EventList([]),
        }


class EventList:
    def __init__(self, actions: list) -> None:
        self.head = EventNode(None)
        self.tail = self.head
        for action in actions:
            self.append(action)
    
    def append(self, action) -> EventNode:
        self.tail.next = EventNode(action, self.tail)
        self.tail = self.tail.next
        return self.tail

    def on_call(self, game: GeniusGame) -> None:
        node = self.head.next
        while node:
            node.on_call(game)
            node = node.next



'''
事件种类
'''

class EventManager:
    def __init__(self) -> None:
        self.events = defaultdict(EventListDict)
    
    def register(self, event_name, event_type, action) -> EventNode:
        return self.events[event_name][event_type].append(action)
    
    def invoke(self, event_name, game: GeniusGame) -> None:
        for event_type in self.events[event_name]:
            self.events[event_name][event_type].on_call(game)





# class OnDealDamageEvent(EventNode):


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