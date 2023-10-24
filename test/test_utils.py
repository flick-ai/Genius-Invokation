from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *

#常用操作
def end_round() -> Action:
    '''
    结束回合
    '''
    return Action(15, 1, [])

def choose_dice_empty() -> Action:
    '''
    投掷骰子，不选择骰子
    '''
    return Action(16, 13, [])

def choose_cards_empty() -> Action:
    '''
    制衡手牌，不选择卡牌
    '''
    return Action(17, 14, [])

def choose_character_default(game:GeniusGame) -> Action:
    '''
    选择出战角色，选择场上最靠前的存活角色
    '''
    for (index, character) in enumerate(game.active_player.character_list):
        if character.is_alive:
            return choose_character(index)

def passive_action(game:GeniusGame) -> Action:
    '''
    返回当前局面下的被动操作
    结束回合，不替换手牌，不重掷骰子，在需要选择出战角色时选择场上最靠前的存活角色
    '''
    mask, use_dice = game.active_player.action_mask[:,:,0], game.active_player.action_mask[:,:,1:]
    choose_list = []
    last_choice = -1
    mask_sum = mask.sum(axis=1)
    for i in range(18):
        if mask_sum[i] >= 1:
            choose_list.append(i)
            last_choice = i
    choice = last_choice
    if last_choice == 17:
        return choose_cards_empty()
    if last_choice == 16:
        return choose_dice_empty()
    if last_choice == 15:
        return end_round()
    if last_choice == 14:
        return choose_character_default(game)