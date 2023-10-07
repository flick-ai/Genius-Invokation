'''
    definition of action space
    consist of three stage of actions: choice, target and dice
'''

from enum import Enum

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
'''

'''
    dice action (n dim), for each dim
    0-16: the i th dice
'''