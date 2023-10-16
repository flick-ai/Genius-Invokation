'''
    definition of action space
    consist of three stage of actions: choice, target and dice
'''

from utils import *

'''
    choice action (1 dim)
    0-9: 10 hand cards (from left to right)
    10-13: 4 character skills
    14: change character
    15: pass this turn
    16: dice region
    17: card region

'''
# 16: none (to solve problem caused by "Toss-up" and "Nature and Wisdom" and so on)

'''
    target action (1 dim)
    0: opponent
    1: myself or none
    2-4: my characters (from left to right)
    5-8: opponent summon region
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
        '''
        if 0 <= self.choice < 10:
            self.choice_type = ActionChoice.HAND_CARD
            self.choice_idx = self.choice
        elif 10 <= self.choice < 14:
            self.choice_type = ActionChoice.CHARACTER_SKILL
            self.choice_idx = self.choice - 10
        elif self.choice == 14:
            self.choice_type = ActionChoice.CHANGE_CHARACTER
            self.choice_idx = -1
        elif self.choice == 15:
            self.choice_type = ActionChoice.PASS
            self.target_idx = -1
        elif self.choice == 16 or self.choice == 17:
            self.choice_type = ActionChoice.NONE
            self.choice_idx = -1

        if self.target == 0:
                self.target_type = ActionTarget.OPPONENT
                self.target_idx = -1
        elif self.target == 1:
            self.target_type = ActionTarget.MYSELF
            self.target_idx = -1
        elif 2 <= self.target < 5:
            self.target_type = ActionTarget.MY_CHARACTER
            self.target_idx = self.target - 2
        elif 5 <= self.target < 9:
            self.target_type = ActionTarget.OPPONENT_SUMMON
            self.target_idx = self.target - 5
        elif 9 <= self.target < 13:
            self.target = ActionTarget.MY_SUPPORT_REGION
            self.target_idx = self.target - 9
        elif self.target == 13:
            self.target_type = ActionTarget.DICE_REGION
            self.target_idx = -1
        elif self.target == 14:
            self.target_type = ActionTarget.CARD_REGION
            self.target_idx = -1

    @staticmethod
    def from_tuple(action: tuple):
        '''
            (1, 1, list(n))
        '''
        return Action(action[0], action[1], action[2])

    @staticmethod
    def from_input():
        choose_prompt = "请输入一个数字表示你的行动选择:\n打出手牌请选择0-9;\n使用技能请选择10-13;\n切换角色请选择14;\n回合结束请选择15;\n其他行动请选择16\n"
        choose = int(input(choose_prompt))
        target_prompt = "请输入一个数字表示你的行动目标:\n选择对方请选择0;\n选择本方请选择1;\n选择角色请选择2-4;\n对手召唤请选择5-8;\n本方支援请选择9-12\n;本方骰子请选择13\n;本方手牌请选择14\n"
        target = int(input(target_prompt))
        list_prompt = "请输入一个形如0 1 2的列表列表表征你选择的位置,主要用于选择骰子,特殊情况表示手牌:\n"
        dice = input(list_prompt)
        dice = [int(i) for i in dice.split(' ')]
        return Action(choose, target, dice)

def choose_card(card: List[int]):
    return Action(17, 14, card)

def choose_dice(dice: List[int]):
    return Action(16, 13, dice)

def choose_character(idx: int):
    return Action(14, idx+2, dice=[])