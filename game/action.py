'''
    definition of action space
    consist of three stage of actions: choice, target and dice
'''

from enum import Enum
from utils import *

'''
    choice action (1 dim)
    0-9: 10 hand cards (from left to right)
    10-13: 4 character skills
    14: change character
    15: pass this turn
    16: none (to solve problem caused by "Toss-up" and "Nature and Wisdom" and so on)
'''

'''
    target action (1 dim)
    0: opponent
    1: myself or none
    2-4: my characters (from left to right)
    5-8: opponent summons
    9-12: my support region
    13: dice region
    14: card region
'''

'''
    multi action (n dim), for each dim
    0-16: the i th dice
'''

# class Action:
#     def __init__(self) -> None:
        

class Action:
    def __init__(self, choice, target, dice) -> None:
        self.choice: int = choice
        self.target: int = target
        self.choice_list: list(int) = dice

        self.choice_type: ActionChoice
        self.target_type: ActionTarget

        self.choice_idx: int
        self.target_idx: int

        self.set_type()

    
    def set_type(self) -> None:
        '''
            将Action从Tuple形式解码
            TODO: ActionTarget and set index
        '''
        if 0 <= self.choice < 10:
            self.choice_type = ActionChoice.HAND_CARD
        elif 10 <= self.choice < 14:
            self.choice_type = ActionChoice.CHARACTER_SKILL
        elif self.choice == 14:
            self.choice_type = ActionChoice.CHANGE_CHARACTER
            self.target_idx = self.target - 2
        elif self.choice == 15:
            self.choice_type = ActionChoice.PASS
        elif self.choice == 16:
            self.choice_type = ActionChoice.NONE
    
    @staticmethod
    def from_tuple(action: tuple):
        '''
            (1, 1, list(n))
        '''
        return Action(action[0], action[1], action[2])
    
def choose_card(card: List[int]):
    return Action(16, 14, card)

def choose_dice(dice: List[int]):
    return Action(16, 13, dice)

def choose_character(idx: int):
    return Action(14, idx+2, dice=[])