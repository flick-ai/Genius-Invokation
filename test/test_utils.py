from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import Action

#常用操作
def end_round():
    '''
    结束回合
    '''
    return Action(15, 1, [])

def roll_dice_empty():
    '''
    投掷骰子，不选择骰子
    '''
    return Action(16, 13, [])

def switch_cards_empty():
    '''
    制衡手牌，不选择卡牌
    '''
    return Action(17, 14, [])
