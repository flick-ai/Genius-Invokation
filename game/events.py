from card.character.base import Damage
from game.game import GeniusGame


class Events:
    def __init__(self) -> None:
        pass

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


class EventListDict:
    def __init__(self) -> None:
        pass


class EventList:
    def __init__(self, events: list) -> None:
        self.head = EventNode(None)
        self.tail = self.head
        for event in events:
            self.append(event)
    
    def append(self, event):
        self.tail.next = EventNode(event, self.tail)
        self.tail = self.tail.next



'''
事件种类
'''
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